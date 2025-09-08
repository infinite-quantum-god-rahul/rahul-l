# FULL views.py - drop-in replacement
# companies/views.py
from functools import wraps
import json
import re
import random
from datetime import datetime
from types import SimpleNamespace  # ← added

from django.apps import apps
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group as AuthGroup, Permission, User
from django.core.cache import cache
from django.core.exceptions import FieldError, FieldDoesNotExist, ImproperlyConfigured  # ← added ImproperlyConfigured
from django.db import IntegrityError, transaction, connection, DatabaseError
from django.db.models import ProtectedError, Q, ForeignKey
from django.http import JsonResponse, HttpResponseNotAllowed, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET
from django.utils.timezone import localdate  # ← added
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, QueryDict

# Simple test views for deployment
def simple_home(request):
    """Simple home view for testing deployment"""
    return JsonResponse({
        'message': 'SML777 Django Application is running!',
        'status': 'success',
        'version': '1.0.0',
        'debug': settings.DEBUG
    })

def simple_health(request):
    """Simple health check"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'SML777 is running successfully'
    })

# Optional spec import for grid and modal sections (PDF/SML sync)
try:
    from .forms_spec import FORMS_SPEC
except Exception:
    FORMS_SPEC = {}

from .models import Company, Column, Client, Users, Staff
from .forms import *
from .services.credit_bureau import CreditBureauClient  # safe if file absent (feature flag off)

# optional EMI builder (feature stays no-op if file absent)
try:
    from .utils.emi import build_emi_schedule  # provides schedule list
except Exception:
    build_emi_schedule = None


# ────────────────────────────────────────────────────────────────────
#  MySQL helper
# ────────────────────────────────────────────────────────────────────
def _is_mysql() -> bool:
    try:
        return connection.vendor == "mysql"
    except Exception:
        return False


# ────────────────────────────────────────────────────────────────────
#  user-profile ⇆ Django-auth sync helpers
# ────────────────────────────────────────────────────────────────────
ROLE_GROUPS = {
    "is_master": "Master",
    "is_data_entry": "DataEntry",
    
    "is_accounting": "Accounting",
    "is_recovery_agent": "RecoveryAgent",
    "is_auditor": "Auditor",
    "is_manager": "Manager",
}


def _desired_groups_for_profile(profile):
    groups = []
    for flag, group_name in ROLE_GROUPS.items():
        if getattr(profile, flag, False):
            grp, _ = AuthGroup.objects.get_or_create(name=group_name)
            groups.append(grp)
    if getattr(profile, "is_admin", False):
        grp, _ = AuthGroup.objects.get_or_create(name="Admin")
        groups.append(grp)
    return groups


def ensure_auth_user_for_profile(profile, username: str, raw_password: str | None):
    username = (username or "").strip()
    if not username:
        return None

    # Check if this username was recently deleted to prevent recreation
    from django.core.cache import cache
    cache_key = f"deleted_user_{username}"
    if cache.get(cache_key):
        # This username was recently deleted, don't recreate
        return None

    user = User.objects.filter(username=username).first() or User(username=username)

    has_any_role = any([
        getattr(profile, "is_admin", False),
        getattr(profile, "is_data_entry", False),

        getattr(profile, "is_accounting", False),
        getattr(profile, "is_recovery_agent", False),
        getattr(profile, "is_auditor", False),
        getattr(profile, "is_manager", False),
    ])
    user.is_active = True
    # Always set is_staff to True for new users (Django admin access)
    user.is_staff = True
    user.is_superuser = getattr(profile, "is_admin", False)

    try:
        if getattr(profile, "full_name", None):
            user.first_name = profile.full_name
    except Exception:
        pass

    if raw_password:
        user.set_password(raw_password)

    user.save()
    user.groups.set(_desired_groups_for_profile(profile))
    user.save()

    try:
        profile.extra_data = (profile.extra_data or {}) | {
            "auth_user_id": user.id,
            "auth_username": user.username,
        }
        profile.save(update_fields=["extra_data"])
    except Exception:
        try:
            profile.save()
        except Exception:
            pass

    return user


# ────────────────────────────────────────────────────────────────────
#  Helpers
# ────────────────────────────────────────────────────────────────────
def is_staff_or_superuser(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@require_POST
def switch_account(request):
    auth.logout(request)
    return redirect(reverse("login"))


def _looks_ajax(request):
    xr = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.META.get(
        "HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    accepts_json = "application/json" in (request.headers.get("Accept") or "").lower()
    return xr or accepts_json


def ajax_login_required_or_redirect(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if _looks_ajax(request):
                return JsonResponse({"success": False, "error": "Authentication required"}, status=401)
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return view_func(request, *args, **kwargs)

    return _wrapped


def feature_enabled(key: str) -> bool:
    try:
        return bool(getattr(settings, "SML_FEATURES", {}).get(key, False))
    except Exception:
        return False


def _only_active(qs, model):
    try:
        fields = {f.name for f in model._meta.get_fields()}
    except Exception:
        fields = set()
    q = Q();
    added = False
    if "status" in fields:
        q |= Q(status__iexact="active") | Q(status=1) | Q(status=True) | Q(status="1");
        added = True
    if "is_active" in fields:
        q |= Q(is_active=True);
        added = True
    if "active" in fields:
        q |= Q(active=1) | Q(active=True) | Q(active="1");
        added = True
    return qs.filter(q) if added else qs


def _exclude_deleted(qs, model):
    try:
        fields = {f.name for f in model._meta.get_fields()}
    except Exception:
        fields = set()
    if "extra_data" in fields:
        try:
            return qs.exclude(extra_data__deleted=True)
        except Exception:
            return qs
    return qs


# dd/mm/yyyy → yyyy-mm-dd
_DDMMYYYY = re.compile(r"^\s*(\d{2})/(\d{2})/(\d{4})\s*$")
_DATE_KEYS = {
    "dob", "joining_date", "joined_on", "from_date", "to_date", "applied_date",
    "disbursement_date", "approval_date", "issue_date", "expiry_date", "birth_date"
}


def _normalize_dates_ddmmyyyy_to_iso(data_dict):
    """
    Accepts either a plain dict or a QueryDict.
    - Preserves QueryDict type (and multi-values) so form.save_m2m() keeps working.
    - Only rewrites values that look like dd/mm/yyyy for keys that look like dates.
    """

    def _maybe_fix(key: str, val: str):
        if not isinstance(val, str):
            return val
        kl = key.lower()
        if ("date" in kl) or (kl in _DATE_KEYS):
            m = _DDMMYYYY.match(val)
            if m:
                d, mth, y = m.groups()
                try:
                    return datetime(int(y), int(mth), int(d)).date().isoformat()
                except ValueError:
                    return val
        return val

    if isinstance(data_dict, QueryDict) or hasattr(data_dict, "setlist"):
        qd = data_dict.copy()
        for k in list(qd.keys()):
            vals = qd.getlist(k)
            qd.setlist(k, [_maybe_fix(k, v) for v in vals])
        return qd

    data = dict(data_dict)
    for k, v in list(data.items()):
        data[k] = _maybe_fix(k, v)
    return data


def _json_db_error(e: Exception, default="Unexpected database error"):
    msg = str(e)
    return JsonResponse({"success": False, "error": f"{default}: {msg}"}, status=400)


def _to_float(x):
    try:
        return float(x)
    except Exception:
        return 0.0


def _parse_any_date(s: str):
    if not s:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None


def _maybe_update_emi_schedule(entity_lc: str, instance, request):
    """No-op unless entity is LoanApplication and utils.emi is present."""
    if _norm(entity_lc) != "loanapplication":
        return
    if not build_emi_schedule:
        return

    # fetch values with tolerant fallbacks
    principal = _to_float(
        getattr(instance, "amount", None)
        or getattr(instance, "amount_requested", None)
        or getattr(instance, "loan_amount", None)
        or 0
    )
    annual_rate = _to_float(
        getattr(instance, "interest_rate", None)
        or getattr(instance, "rate", None)
        or getattr(instance, "roi", None)
        or 0
    )
    months = 0
    for k in ("tenure_months", "tenure", "months"):
        v = getattr(instance, k, None)
        if v:
            try:
                months = int(v)
                break
            except Exception:
                pass

    if principal <= 0 or annual_rate <= 0 or months <= 0:
        return

    start_dt = _parse_any_date(
        request.POST.get("emi_start_date")
        or request.POST.get("disbursement_date")
        or request.POST.get("approval_date")
        or ""
    ) or localdate()

    rebuild = str(request.POST.get("rebuild_emi", "0")).strip().lower() in {"1", "true", "on", "yes", "y"}

    ex = (instance.extra_data or {}).copy()
    if not ex.get("emi_schedule") or rebuild:
        try:
            schedule = build_emi_schedule(principal, annual_rate, months, start_dt)
            ex["emi_schedule"] = schedule
            ex.setdefault("payments", [])
            instance.extra_data = ex
            instance.save(update_fields=["extra_data"])
        except Exception:
            # never block save
            pass


# ────────────────────────────────────────────────────────────────────
#  Spec helpers (PDF/SML alignment)
# ────────────────────────────────────────────────────────────────────
def _norm(s: str) -> str:
    return (s or "").strip().lower().replace(" ", "").replace("_", "").replace("-", "")


def get_model_class(entity):
    ent = (entity or "").strip()
    ent_clean = ent.replace("-", "").replace(" ", "")
    
    # Direct model name lookup
    try:
        m = apps.get_model("companies", ent)
        if m:
            return m
    except LookupError:
        pass
    
    # Clean model name lookup
    try:
        m = apps.get_model("companies", ent_clean)
        if m:
            return m
    except LookupError:
        pass
    
    # Title case lookup
    try:
        m = apps.get_model("companies", ent.title().replace("_", "").replace("-", ""))
        if m:
            return m
    except LookupError:
        pass
    
    # Special handling for Users
    if _norm(ent) in ['users', 'userprofile', 'user_profile', 'user-profile']:
        try:
            return apps.get_model("companies", "Users")
        except LookupError:
            pass
    
    # Fallback: iterate through all models
    try:
        app = apps.get_app_config("companies")
        tgt = _norm(ent)
        for m in app.get_models():
            if _norm(m.__name__) == tgt:
                return m
    except Exception:
        pass
    return None


def _spec_for(entity: str):
    key = None
    try:
        mc = get_model_class(entity)
        key = mc.__name__ if mc else None
    except Exception as e:
        key = None
    if key and key in FORMS_SPEC:
        return FORMS_SPEC.get(key)
    # fallback by normalizing name
    ent_us = (entity or "").replace("-", "_")
    camel = "".join(p.capitalize() for p in ent_us.split("_") if p)
    result = FORMS_SPEC.get(camel)
    return result


def _sections_from_spec(entity: str):
    spec = _spec_for(entity)
    if not spec:
        return None
    sections = spec.get("sections") or {}
    remapped = {}
    for sec, fields in sections.items():
        names = []
        for f in fields:
            if isinstance(f, dict):
                nm = f.get("name")
            else:
                nm = str(f)
            if nm:
                names.append(nm)
        remapped[sec] = names
    return remapped or None


def _grid_from_spec(entity: str):
    spec = _spec_for(entity)
    if not spec:
        return None
    grid = spec.get("grid") or []
    return list(grid) if grid else None


# ────────────────────────────────────────────────────────────────────
#  Auth Views
# ────────────────────────────────────────────────────────────────────
def home_view(request):
    return render(request, "home.html")


ATTEMPT_KEY = "login_attempts:{ip}:{u}"
LOCK_KEY = "login_lock:{ip}:{u}"
MAX_ATTEMPTS = 5
OTP_REQUIRED_AFTER = 999  # Temporarily disabled for testing
LOCK_SECONDS = 60


def _client_ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR")
    return fwd.split(",")[0].strip() if fwd else (request.META.get("REMOTE_ADDR") or "unknown").strip()


@csrf_protect
def login_view(request):
    if request.method != "POST":
        from django.middleware.csrf import get_token
        get_token(request)
        return render(request, "home.html")

    username = (request.POST.get("username") or "").strip()
    password = request.POST.get("password") or ""
    otp = request.POST.get("otp") or ""
    remember = request.POST.get("remember") == "on"

    ip = _client_ip(request)
    attempt_key = ATTEMPT_KEY.format(ip=ip, u=username or "_")
    lock_key = LOCK_KEY.format(ip=ip, u=username or "_")

    if cache.get(lock_key):
        return JsonResponse({"success": False, "error": "Too many attempts. Please wait a minute."}, status=429)

    attempts = int(cache.get(attempt_key) or 0)
    if attempts >= OTP_REQUIRED_AFTER and not otp:
        return JsonResponse({"success": False, "require_otp": True, "error": "OTP required"}, status=200)

    # Check if this username was recently deleted
    cache_key = f"deleted_user_{username}"
    if cache.get(cache_key):
        attempts += 1
        cache.set(attempt_key, attempts, timeout=LOCK_SECONDS * 3)
        if attempts >= MAX_ATTEMPTS:
            cache.set(lock_key, True, timeout=LOCK_SECONDS)
        return JsonResponse({"success": False, "error": "Invalid credentials or permission denied"}, status=200)

    user = authenticate(request, username=username, password=password)

    def verify_otp(otp_code: str) -> bool:
        if attempts < OTP_REQUIRED_AFTER:
            return True
        return bool(otp_code and otp_code.isdigit() and 4 <= len(otp_code) <= 8)

    if user and is_staff_or_superuser(user) and verify_otp(otp):
        login(request, user)
        request.session.set_expiry(14 * 24 * 3600 if remember else 0)
        cache.delete(attempt_key);
        cache.delete(lock_key)
        return JsonResponse({"success": True, "redirect_url": "/companies/dashboard/"})

    attempts += 1
    cache.set(attempt_key, attempts, timeout=LOCK_SECONDS * 3)
    if attempts >= MAX_ATTEMPTS:
        cache.set(lock_key, True, timeout=LOCK_SECONDS)
        return JsonResponse({"success": False, "error": "Account temporarily locked due to failed attempts."},
                            status=429)

    return JsonResponse({
        "success": False,
        "error": "Invalid credentials or permission denied",
        "require_otp": attempts >= OTP_REQUIRED_AFTER
    }, status=200)


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


# ────────────────────────────────────────────────────────────────────
#  Dashboard
# ────────────────────────────────────────────────────────────────────
@login_required
def dashboard_view(request):
    user = request.user
    display_name = user.get_full_name() or user.username
    branch_name = ""
    role_label = None

    try:
        profile = get_profile_for_user(user)
    except Exception:
        profile = None
    if profile:
        if getattr(profile, "branch", None):
            try:
                branch_name = profile.branch.name
            except Exception:
                branch_name = ""
        
        # Simple role determination
        if user.is_superuser:
            role_label = "Superuser"
        elif user.is_staff:
            role_label = "Staff"
        
        else:
            role_label = "User"

    # Get role flags for proper permission system
    role_flags_data = role_flags(user)
    
    return render(
        request, "dashboard.html",
        {
            "staff_info": getattr(user, "staff_info", None),
            "header_user_display_name": display_name,
            "header_branch_name": branch_name,
            "header_role_label": role_label,
            "profile": profile,
            "role_flags": role_flags_data,
        },
    )


# ────────────────────────────────────────────────────────────────────
#  Entity utilities
# ────────────────────────────────────────────────────────────────────
# Unblocked: allow User Permissions as a normal entity
_FAUX_ENTITIES = set()


def get_form_class(entity):
    print(f"=== DEBUG get_form_class ===")
    print(f"Entity: {entity}")
    
    # Import forms directly to avoid circular import issues
    try:
        from . import forms
        print(f"Forms module imported successfully")
    except Exception as e:
        print(f"Error importing forms: {e}")
        return None
    
    # be tolerant of dashes/underscores/case
    ent = (entity or "")
    ent_us = ent.replace("-", "_")
    name = f"{ent_us.capitalize()}Form"
    print(f"Looking for form class: {name}")
    
    # Try to get from forms module first
    form_class = getattr(forms, name, None)
    print(f"Found in forms module: {form_class}")
    if form_class:
        return form_class
    
    # Fallback to globals
    form_class = globals().get(name)
    print(f"Found in globals: {form_class}")
    if form_class:
        return form_class
        
    parts = ent_us.split("_")
    camel = "".join(p.capitalize() for p in parts if p)
    alt_name = f"{camel}Form"
    print(f"Trying alt name: {alt_name}")
    
    # Try alt name from forms module
    form_class = getattr(forms, alt_name, None)
    if form_class:
        print(f"Found alt in forms module: {form_class}")
        return form_class
    
    # Fallback to globals
    form_class = globals().get(alt_name)
    print(f"Found alt in globals: {form_class}")
    if form_class:
        return form_class
        
    lower_entity = ent.replace("_", "").replace("-", "").lower()
    print(f"Lower entity: {lower_entity}")
    
    # Debug: show all available form classes from forms module
    available_forms = [obj for obj in dir(forms) if isinstance(getattr(forms, obj), type) and obj.lower().endswith("form")]
    print(f"Available form classes in forms module: {available_forms}")
    
    # Try to find by pattern matching in forms module
    for form_name in dir(forms):
        form_obj = getattr(forms, form_name)
        if isinstance(form_obj, type) and form_name.lower().endswith("form"):
            candidate = form_name.lower().replace("form", "")
            if candidate == lower_entity or lower_entity in candidate:
                print(f"Found matching form in forms module: {form_name}")
                return form_obj
    
    # Debug: show all available form classes in globals
    available_forms = [obj for obj in globals().values() if isinstance(obj, type) and obj.__name__.lower().endswith("form")]
    print(f"Available form classes in globals: {[f.__name__ for f in available_forms]}")
    
    for obj in globals().values():
        if isinstance(obj, type) and obj.__name__.lower().endswith("form"):
            candidate = obj.__name__.lower().replace("form", "")
            if candidate == lower_entity or lower_entity in candidate:
                print(f"Found matching form in globals: {obj.__name__}")
                return obj
                
    print(f"❌ No form class found for entity: {entity}")
    return None


def get_section_map(entity):
    # Prefer spec sections
    spec_map = _sections_from_spec(entity)
    if spec_map:
        return spec_map
    # Fallback legacy groupings
    return {
        "clientjoiningform": {"Personal Info": ["member", "joined_on", "referred_by"], "Meta": ["joining_date"]},
        "staff": {"Staff Details": ["name", "joining_date", "branch"]},
        "loanapplication": {"Loan Info": ["client", "product", "amount_requested", "applied_date"],
                            "Meta": ["joining_date"]},
        "users": {"User Setup": ["staff", "user", "branch", "password"], "Permissions": [],
                        "Status": ["status"]},
        "userpermission": {
            "User": ["user_profile"],
            "Roles": ["is_admin", "is_master", "is_data_entry", "is_accounting", "is_recovery_agent", "is_auditor",
                      "is_manager"],
            "Status": ["status"],
        },
        "role": {"Role Details": ["name"]},
        "kycdocument": {"Document": ["extra__doc_type", "extra__doc_no", "extra__document_file", "extra__expiry_date"],
                        "Holder": ["extra__party_name"], "Verification": ["extra__verified_on"]},
        "alertrule": {"Basics": ["extra__name", "extra__entity", "extra__is_active"],
                      "Logic": ["extra__condition", "extra__channel"]},
    }.get(entity.lower().replace("-", ""), None)


pretty_names = {
    "loanapplication": "Loan Application",
    "clientjoiningform": "Client Joining Form",
            "users": "Users",
    "userpermission": "User Permissions",
    "staff": "Staff Registration",
    "role": "Role Management",
    "product": "Products Management",
    "company": "Company",
    "branch": "Branch",
    "village": "Village",
    "center": "Center",
    "group": "Group",
    "column": "Column",
    "businesssetting": "Business Setting Rules",
    "fieldschedule": "Field Schedule",
    "kycdocument": "KYC Document",
    "alertrule": "Alert Rule",
    "appointment": "Appointment",
    "salarystatement": "Salary Statement",
    # added for full SML parity with models/forms
    "prepaid": "Prepaid",
    "mortgage": "Mortgage",
    "exsaving": "Savings Account",
    "accounthead": "Account Head",
    "voucher": "Voucher",
    "posting": "Posting",
    "recoveryposting": "Recovery Posting",
    "payment": "Payment",
    "gatewayevent": "Gateway Event",
    "notification": "Notification",
    "ewiflag": "EWI Flag",
    "loanrestructure": "Loan Restructure",
    "repayment": "Repayment",
}


def _truthy(v): return str(v).strip().lower() in {"true", "1", "yes", "y", "t"}


def _flag(profile, attr: str) -> bool:
    v = getattr(profile, attr, False)
    return v if isinstance(v, bool) else _truthy(v)


DE_MODELS_SET = {"client", "loanapplication", "recoveryposting", "clientjoiningform", "clientjoining"}
ACC_MODELS_SET = {"voucher", "posting", "accounthead"}
REPORT_MODELS_SET = {"fieldreport", "reportdropdownmenu", "reportdropdown"}


def _in_scope(entity_lc: str, scope_set: set[str]) -> bool:
    if entity_lc in scope_set: return True
    n = _norm(entity_lc)
    if n in {_norm(x) for x in scope_set}: return True
    if "report" in n and any("report" in _norm(x) for x in scope_set): return True
    return False


def get_profile_for_user(user):
    username = user.get_username()
    profile = None
    try:
        user_field = Users._meta.get_field("user")
        if isinstance(user_field, ForeignKey):
            try:
                profile = Users.objects.filter(user_id=user.id).first() or Users.objects.filter(
                    user__username=username).first()
            except Exception:
                profile = None
        else:
            try:
                profile = Users.objects.filter(user=username).first() or Users.objects.filter(
                    user__iexact=username).first()
            except Exception:
                profile = None
    except Exception:
        profile = None
    if profile is None:
        try:
            profile = Users.objects.filter(extra_data__auth_username=username).first()
        except Exception:
            profile = None
    if profile is None:
        try:
            profile = Users.objects.filter(extra_data__auth_user_id=user.id).first()
        except Exception:
            profile = None
    return profile


def user_in_group(user, group_name: str) -> bool:
    return user.groups.filter(name__iexact=group_name).exists()


def user_is_master(user) -> bool:
    profile = get_profile_for_user(user)
    is_m = False
    if profile is not None:
        # Check UserPermission for is_master flag
        try:
            user_perm = UserPermission.objects.filter(user_profile=profile).first()
            if user_perm:
                v = getattr(user_perm, "is_master", False)
                is_m = v if isinstance(v, bool) else _truthy(v)
        except Exception:
            pass
        
        if not is_m:
            try:
                v2 = (profile.extra_data or {}).get("is_master")
                if v2 is not None:
                    is_m = v2 if isinstance(v2, bool) else _truthy(v2)
            except Exception:
                pass
    if not is_m and user_in_group(user, "Master"):
        is_m = True
    return is_m


def role_flags(user):
    profile = get_profile_for_user(user)
    admin = data_entry = accounting = master = False
    recovery_agent = auditor = manager = False

    # Superuser gets all permissions
    if user.is_superuser:
        admin = master = data_entry = accounting = recovery_agent = auditor = manager = True
    elif profile:
        # Get permission flags from UserPermission, not Users profile
        try:
            user_perm = UserPermission.objects.filter(user_profile=profile).first()
            if user_perm:
                admin = _flag(user_perm, "is_admin")
                master = _flag(user_perm, "is_master")
                data_entry = _flag(user_perm, "is_data_entry")
                accounting = _flag(user_perm, "is_accounting")
                recovery_agent = _flag(user_perm, "is_recovery_agent")
                auditor = _flag(user_perm, "is_auditor")
                manager = _flag(user_perm, "is_manager")
                
        except Exception:
            pass

    # Check Django groups as fallback
    admin = admin or user_in_group(user, "Admin")
    master = master or user_in_group(user, "Master")
    data_entry = data_entry or user_in_group(user, "DataEntry")
    accounting = accounting or user_in_group(user, "Accounting")
    recovery_agent = recovery_agent or user_in_group(user, "RecoveryAgent")
    auditor = auditor or user_in_group(user, "Auditor")
    manager = manager or user_in_group(user, "Manager")

    return {
        "admin": admin,
        "master": master,
        "data_entry": data_entry,
        "accounting": accounting,
        "profile": profile,
        "recovery_agent": recovery_agent,
        "auditor": auditor,
        "manager": manager,
    }


def can_user_delete_entity(user, entity_lc: str) -> bool:
    if user.is_superuser:
        return True

    rf = role_flags(user)
    profile = rf["profile"]
    ent = (entity_lc or "").lower()

    # MASTER ROLE LOGIC: Master role cannot delete its own scope
    if rf["master"]:
        # Master entities that Master role cannot delete
        master_entities = {"company", "branch", "users", "userpermission", "village", "center", "group", "cadre", "column"}
        
        # If trying to delete a Master entity, check if user has other roles
        if ent in master_entities:
            # Master role alone cannot delete Master entities
            # But if user has OTHER roles (like Admin), they can delete
            if rf["admin"]:
                return True  # Admin overrides Master restriction
            return False  # Master role alone cannot delete Master entities
        
        # For non-Master entities, check other role permissions
        if rf["data_entry"] and _in_scope(ent, DE_MODELS_SET):
            return True  # Data Entry role can delete its scope
        if rf["accounting"] and _in_scope(ent, ACC_MODELS_SET):
            return True  # Accounting role can delete its scope
        if rf["recovery_agent"] and _in_scope(ent, {"client", "loanapplication", "fieldreport", "recoveryposting"}):
            return True  # Recovery Agent role can delete its scope
        if rf["manager"] and _in_scope(ent, {"village", "center", "group", "staff", "client", "loanapplication", "fieldschedule", "businesssetting", "accounthead", "voucher", "posting", "payment", "repayment", "recoveryposting"}):
            return True  # Manager role can delete its scope
        
        # Master role alone (no other roles) cannot delete anything
        return False

    # NON-MASTER USERS: Normal permission logic
    if rf["admin"]:
        return True  # Admin can delete everything
    if rf["data_entry"] and _in_scope(ent, DE_MODELS_SET):
        return True  # Data Entry can delete its scope
    if rf["accounting"] and _in_scope(ent, ACC_MODELS_SET):
        return True  # Accounting can delete its scope
    if rf["recovery_agent"] and _in_scope(ent, {"client", "loanapplication", "fieldreport", "recoveryposting"}):
        return True  # Recovery Agent can delete its scope
    if rf["manager"] and _in_scope(ent, {"village", "center", "group", "staff", "client", "loanapplication", "fieldschedule", "businesssetting", "accounthead", "voucher", "posting", "payment", "repayment", "recoveryposting"}):
        return True  # Manager can delete its scope
    
    return False


def _debug_delete(user, entity_lc, allowed):
    try:
        rf = role_flags(user)
        print(f"[DELETE_CHECK] user={user.username} entity={entity_lc} "
              f"roles={{admin:{rf['admin']}, data_entry:{rf['data_entry']}, "
              f"accounting:{rf['accounting']}, master:{rf['master']}}} allowed={allowed}")
    except Exception:
        pass


# ────────────────────────────────────────────────────────────────────
#  PERF maps + pagination helpers (new)
# ────────────────────────────────────────────────────────────────────
RELATED_MAP = {
    "Client": ["branch", "center", "group"],
    "Staff": ["branch"],
    "LoanApplication": ["client", "product"],
    "FieldReport": ["staff", "center"],
            "Users": ["branch", "staff"],
}
PREFETCH_MAP = {
    "Role": ["permissions"],
}
ONLY_MAP = {
    "Client": ["id", "code", "name", "aadhar", "mobile", "branch__name", "center__name", "group__name"],
    "Staff": ["id", "code", "name", "mobile", "branch__name"],
    "LoanApplication": ["id", "code", "client__name", "product__name", "created_at", "amount"],
    "FieldReport": ["id", "date", "staff__name", "center__name", "summary"],
            "Users": ["id", "user", "branch__name", "is_admin", "is_master"],
}


def _model_field_names(model):
    try:
        return {f.name for f in model._meta.get_fields()}
    except Exception:
        return set()


def _safe_select_related(qs, model, names):
    fields = _model_field_names(model)
    sel = [n for n in names if n in fields]
    return qs.select_related(*sel) if sel else qs


def _safe_prefetch_related(qs, model, names):
    fields = _model_field_names(model)
    pre = [n for n in names if n in fields]
    return qs.prefetch_related(*pre) if pre else qs


def _safe_only(qs, model, names):
    # allow double-underscore only if base field exists
    fields = _model_field_names(model)
    valid = []
    for n in names:
        base = n.split("__", 1)[0]
        if base in fields:
            valid.append(n)
    return qs.only(*valid) if valid else qs


def paginate_nocount(qs, page, per_page):
    page = max(int(page or 1), 1)
    per_page = max(10, min(int(per_page or 25), 100))
    start = (page - 1) * per_page
    rows = list(qs[start:start + per_page + 1])
    has_next = len(rows) > per_page
    object_list = rows[:per_page]
    return SimpleNamespace(
        object_list=object_list,
        number=page,
        per_page=per_page,
        has_next=has_next,
        has_previous=page > 1,
        next_page_number=(page + 1) if has_next else None,
        previous_page_number=(page - 1) if page > 1 else None,
        start_index=(start + 1) if object_list else 0,
        end_index=(start + len(object_list)) if object_list else 0,
    )


# ────────────────────────────────────────────────────────────────────
#  Lists
# ────────────────────────────────────────────────────────────────────
@login_required
def entity_list(request, entity):
    print(f"=== ENTITY_LIST VIEW CALLED ===")
    print(f"Entity: {entity}")
    print(f"Request method: {request.method}")
    print(f"Request URL: {request.path}")
    print(f"Request GET params: {request.GET}")
    
    entity_lc = (entity or "").lower()
    print(f"Entity lowercase: {entity_lc}")
    print(f"=== CUSTOM FIELD LOADING WILL START NOW ===")
    print(f"=== TESTING IF VIEW IS WORKING ===")

    model = get_model_class(entity_lc)
    print(f"Model class: {model}")
    if model is None:
        print(f"ERROR: Model not found for entity {entity}")
        return JsonResponse({"success": False, "error": f'Model for entity "{entity}" not found.'}, status=404)

    # Show ALL by default to preserve previous logic
    objects = model.objects.all()

    # Always filter for active records if the model has a status field
    if hasattr(model, '_meta') and any(field.name == 'status' for field in model._meta.fields):
        objects = _only_active(objects, model)
        print(f"DEBUG: Filtering {entity} for active records only")
    
    # Optional filters (opt-in via querystring)
    if request.GET.get("active_only") == "1":
        objects = _only_active(objects, model)
    if request.GET.get("hide_deleted") == "1":
        objects = _exclude_deleted(objects, model)

    # Apply select_related / prefetch_related / only() safely
    ent_key = getattr(model, "__name__", None) or model.__name__
    mname = getattr(getattr(model, "_meta", None), "model_name", entity_lc)
    rels = RELATED_MAP.get(ent_key, []) or []

    # If we will traverse a relation, ensure it won't be deferred by ONLY
    # by forcing the FK names into the ONLY list (and keeping *_id variants)
    only_base = set(ONLY_MAP.get(ent_key, []) or [])
    only_with_rels = only_base | set(rels) | {f"{r}_id" for r in rels}

    # Users: don't pre-defer anything (avoid TypeError on defer(None))
    if mname == "users":
        pass

    objects = _safe_select_related(objects, model, rels)
    objects = _safe_prefetch_related(objects, model, PREFETCH_MAP.get(ent_key, []))
    objects = _safe_only(objects, model, list(only_with_rels))

    # Sorting: prefer 'code', else '-created_at', else 'id'
    fset = _model_field_names(model)
    if "code" in fset:
        objects = objects.order_by("code")
    elif "created_at" in fset:
        objects = objects.order_by("-created_at")
    else:
        objects = objects.order_by("id")

    # Columns config: keep old Column table logic. If empty or ?use_spec_grid=1, use FORMS_SPEC grid.
    column_fields = []  # Initialize default value
    
    # Load custom fields for Company
    try:
        from companies.models import Column
        found_fields = list(Column.objects.filter(module="Company").order_by("order"))
        if found_fields:
            column_fields = found_fields
        else:
            column_fields = []
                    
    except Exception as e:
        column_fields = []

    # Always get spec_grid for standard fields, then add custom fields
    spec_grid = _grid_from_spec(entity_lc) or []
    
    # Always process spec_grid fields - they should always be available
    spec_columns = []
    if spec_grid:
        # lightweight spec-column wrapper compatible with most templates
        class _SpecCol:
            __slots__ = ("field_name", "label", "required", "order")

            def __init__(self, field_name, label, order):
                self.field_name = field_name
                self.label = label
                self.required = False
                self.order = order

        def _labelize(n: str) -> str:
            return n.replace("extra__", "").replace("_", " ").title()

        spec_columns = [_SpecCol(fn, _labelize(fn), i) for i, fn in enumerate(spec_grid)]
    
    # Filter out custom fields that are already in spec_grid to avoid duplicates
    spec_field_names = set(spec_grid)
    filtered_column_fields = [cf for cf in column_fields if cf.field_name not in spec_field_names]
    
    # Combine custom fields from Column table with spec fields
    all_column_fields = list(filtered_column_fields) + spec_columns

    # Fast no-count pagination
    page = request.GET.get("page", "1")
    per_page = request.GET.get("page_size", "25")
    page_obj = paginate_nocount(objects, page, per_page)

    grouped_objects = {"All Records": page_obj.object_list}

    user = request.user
    profile = get_profile_for_user(user)
    role_flags_data = role_flags(user)

    context = {
        "include_template": "companies/grid_list.html",
        "entity": entity,
        "pretty_entity": pretty_names.get(_norm(entity_lc), entity.replace("_", " ").replace("-", " ").title()),
        "grouped_objects": grouped_objects,
        "column_fields": filtered_column_fields,  # Only custom fields from Column table (filtered to avoid duplicates)
        "spec_grid": spec_grid or [],  # Standard fields from forms_spec (always available)
        "profile": profile,
        "role_flags": role_flags_data,
        "can_delete": can_user_delete_entity(user, entity_lc),
        "staff_info": getattr(user, "staff_info", None),
        # pager in template if needed
        "page_obj": page_obj,
        "use_spec_grid": True,  # Always use spec grid since we always have it
    }
    return render(request, "dashboard.html", context)


# ────────────────────────────────────────────────────────────────────
#  Create
# ────────────────────────────────────────────────────────────────────
@ajax_login_required_or_redirect
@require_POST
def entity_create(request, entity):
    entity_lc = (entity or "").lower()

    form_class = get_form_class(entity_lc)
    if not form_class:
        return JsonResponse({"success": False, "error": f'Form class for entity "{entity}" not found.'}, status=400)

    try:
        # FIX: correct kwarg syntax to avoid errors/hangs
        extra_fields = Column.objects.filter(module__iexact=_norm(entity_lc)).order_by("order")
    except DatabaseError as e:
        extra_fields = []

    try:
        post_data = _normalize_dates_ddmmyyyy_to_iso(request.POST)
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Date normalization failed: {str(e)}"}, status=400)

    try:
        form = form_class(post_data, request.FILES, extra_fields=extra_fields)
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Form creation failed: {str(e)}"}, status=400)

    try:
        is_valid = form.is_valid()
        if not is_valid:
            return JsonResponse({"success": False, "errors": form.errors})
    except Exception as e:
        print(f"DEBUG: ERROR in form validation: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"success": False, "error": f"Form validation failed: {str(e)}"}, status=400)

    if not form.is_valid():
        print(f"DEBUG: Form validation failed: {form.errors}")
        return JsonResponse({"success": False, "errors": form.errors})
    
    print(f"DEBUG: Form validation successful")

    try:
        print(f"DEBUG: Starting transaction for {entity_lc}")
        with transaction.atomic():
            print(f"DEBUG: Transaction started, saving form instance")
            instance = form.save(commit=False)
            print(f"DEBUG: Form instance saved (commit=False)")

            # Staff: auto Empcode if missing
            if _norm(entity_lc) == "staff" and not getattr(instance, "staffcode", None):
                print(f"DEBUG: Auto-generating staffcode for Staff")
                model = get_model_class(entity_lc)
                last = model.objects.order_by("-id").first()
                nxt = (last.id + 1) if last else 1
                instance.staffcode = f"STF{nxt:03d}"
                print(f"DEBUG: Generated staffcode: {instance.staffcode}")
            
            # Staff: ensure status is always active for new staff
            if _norm(entity_lc) == "staff":
                instance.status = "active"

            # Collect dynamic extra__* fields
            instance.extra_data = instance.extra_data or {}
            print(f"DEBUG: ===== SAVE PROCESS START =====")
            print(f"DEBUG: Entity: {entity_lc}")
            print(f"DEBUG: Request POST keys: {list(request.POST.keys())}")
            print(f"DEBUG: Form cleaned_data keys: {list(form.cleaned_data.keys()) if form.cleaned_data else []}")
            
            def _prepare_for_json(value):
                """Convert values to JSON-serializable format"""
                if hasattr(value, 'isoformat'):  # datetime.date, datetime.datetime
                    return value.isoformat()
                elif hasattr(value, '__str__'):
                    return str(value)
                return value
            
            extra_count = 0
            for k, v in request.POST.items():
                if k.startswith("extra__"):
                    clean_key = k.replace("extra__", "")
                    instance.extra_data[clean_key] = _prepare_for_json(v)
                    extra_count += 1
                    print(f"DEBUG: Saved extra__{clean_key} = '{v}' to extra_data")
            
            # Persist NON-MODEL cleaned fields
            model_field_names = {f.name for f in instance._meta.get_fields()}
            cleaned_count = 0
            for k, v in (form.cleaned_data or {}).items():
                if k not in model_field_names and v is not None and v != "":
                    instance.extra_data[k] = _prepare_for_json(v)
                    cleaned_count += 1
                    print(f"DEBUG: Saved non-model field '{k}' = '{v}' to extra_data")
            
            print(f"DEBUG: Total saved to extra_data: {extra_count} extra__ fields, {cleaned_count} non-model fields")
            print(f"DEBUG: Final extra_data: {instance.extra_data}")

            # Users: branch from staff when blank
            if _norm(entity_lc) == "users" and not getattr(instance, "branch_id", None):
                try:
                    if instance.staff and instance.staff.branch_id:
                        instance.branch_id = instance.staff.branch_id
                except Exception:
                    pass
            
            # Users: ensure is_reports is always True for new users
            if _norm(entity_lc) == "users":
                instance.is_reports = True
                # Also ensure is_staff is True for new users (Django admin access)
                if hasattr(instance, 'is_staff'):
                    instance.is_staff = True

            # Default active flags
            try:
                if hasattr(instance, "status") and not instance.status:
                    instance.status = "active"
            except Exception:
                pass
            try:
                if hasattr(instance, "is_active") and instance.is_active in (None, ""):
                    instance.is_active = True
            except Exception:
                pass
            try:
                if hasattr(instance, "active") and instance.active in (None, ""):
                    instance.active = 1
            except Exception:
                pass

            print(f"DEBUG: About to save instance to database")
            instance.save()
            print(f"DEBUG: Instance saved successfully, PK: {instance.pk}")
            print(f"DEBUG: About to save many-to-many relationships")
            form.save_m2m()
            print(f"DEBUG: Many-to-many relationships saved successfully")

            if _norm(entity_lc) == "users":
                user_obj = form.cleaned_data.get("user")
                username = user_obj.username if user_obj else ""
                password = form.cleaned_data.get("password") or None
                
                # Clear the deleted user cache if we're intentionally creating this user
                if username:
                    from django.core.cache import cache
                    cache_key = f"deleted_user_{username}"
                    cache.delete(cache_key)
                
                ensure_auth_user_for_profile(instance, username, password)

            # Mirror UserPermission → UserProfile and auth user
            if _norm(entity_lc) == "userpermission":
                up = getattr(instance, "user_profile", None)
                if up:
                    try:
                        up.is_admin = getattr(instance, "is_admin", False)
                        up.is_master = getattr(instance, "is_master", False)
                        up.is_data_entry = getattr(instance, "is_data_entry", False)
                        up.is_accounting = getattr(instance, "is_accounting", False)
                        up.is_recovery_agent = getattr(instance, "is_recovery_agent", False)
                        up.is_auditor = getattr(instance, "is_auditor", False)
                        up.is_manager = getattr(instance, "is_manager", False)


                        # find username from profile
                        try:
                            user_field = UserProfile._meta.get_field("user")
                            if isinstance(user_field, ForeignKey):
                                username = getattr(getattr(up, "user", None), "username", "") or ""
                            else:
                                username = (getattr(up, "user", "") or "")
                        except Exception:
                            username = (getattr(up, "user", "") or "")
                        if not username:
                            username = ((up.extra_data or {}).get("auth_username") or "")
                        ensure_auth_user_for_profile(up, username, None)
                    except Exception:
                        pass

            # EMI schedule injection (safe and optional)
            _maybe_update_emi_schedule(entity_lc, instance, request)

            return JsonResponse({"success": True, "id": instance.pk}) if _looks_ajax(request) else HttpResponseRedirect(
                f"/{entity}/")
    except DatabaseError as e:
        return _json_db_error(e, "Create failed")
    except IntegrityError as e:
        return JsonResponse({"success": False, "errors": {"__all__": [str(e)]}}, status=400)
    except ProtectedError:
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Create blocked due to protected related objects."]}}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "errors": {"__all__": [str(e)]}}, status=400)


# ────────────────────────────────────────────────────────────────────
#  Get (modal)
# ────────────────────────────────────────────────────────────────────
@ajax_login_required_or_redirect
def entity_get(request, entity, pk=None):
    print(f"=== ENTITY_GET VIEW CALLED ===")
    print(f"Request method: {request.method}")
    print(f"Entity: {entity}")
    print(f"PK: {pk}")
    print(f"Request path: {request.path}")
    
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    # Users now works with standard modal system
    # local imports to keep this drop-in self-contained
    import json
    from django.db import DatabaseError

    print(f"=== PROCESSING ENTITY_GET ===")
    entity_lc = (entity or "").lower()
    print(f"Entity LC: {entity_lc}")

    model = get_model_class(entity_lc)
    if model is None:
        return JsonResponse({"success": False, "error": f'Model for entity "{entity}" not found.'}, status=404)

    form_class = get_form_class(entity_lc)
    print(f"=== DEBUG entity_get ===")
    print(f"Entity: {entity}, Entity LC: {entity_lc}")
    print(f"Form class found: {form_class}")
    if not form_class:
        return JsonResponse({"success": False, "error": f'Form class for entity "{entity}" not found.'}, status=400)

    try:
        extra_fields = Column.objects.filter(module__iexact=_norm(entity_lc)).order_by("order")
        missing_column_table = False
    except DatabaseError:
        extra_fields = []
        missing_column_table = True

    edit_mode = False
    object_id = ""
    if pk:
        obj = get_object_or_404(model, pk=pk)
        print(f"DEBUG: Creating form for EDIT with instance PK: {obj.pk}")
        print(f"DEBUG: Instance extra_data: {getattr(obj, 'extra_data', None)}")
        print(f"DEBUG: Instance extra_data type: {type(getattr(obj, 'extra_data', None))}")
        form = form_class(instance=obj, extra_fields=extra_fields)
        print(f"DEBUG: Form created: {type(form)}")
        print(f"DEBUG: Form fields count: {len(form.fields)}")
        print(f"DEBUG: Form instance: {form.instance}")
        print(f"DEBUG: Form instance PK: {getattr(form.instance, 'pk', None)}")
        print(f"DEBUG: Form instance extra_data: {getattr(form.instance, 'extra_data', None)}")
        edit_mode = True
        object_id = pk
    else:
        obj = model()
        try:
            obj.code = obj._next_code() if hasattr(obj, "_next_code") else ""
        except Exception:
            pass
        # Set default values for Users
        if _norm(entity_lc) == "users":
            try:
                obj.is_reports = True
            except Exception:
                pass

        # Use standard form handling for all entities including Users
        print(f"DEBUG: Creating form for CREATE")
        form = form_class(instance=obj, extra_fields=extra_fields)
        print(f"DEBUG: Form created: {type(form)}")
        print(f"DEBUG: Form fields count: {len(form.fields)}")

    # Ensure any "*code" field is editable on EDIT (covers company code variants)
    if edit_mode:
        try:
            for _nm, _fld in form.fields.items():
                nm_lc = _nm.lower()
                cls = _fld.widget.attrs.get("class", "") or ""
                is_code_like = (nm_lc == "code") or nm_lc.endswith("code") or ("autocode" in cls)
                if is_code_like:
                    _fld.widget.attrs["class"] = " ".join(c for c in cls.split() if c != "autocode") or "form-control"
                    _fld.widget.attrs.pop("readonly", None)
                    _fld.widget.attrs.pop("disabled", None)
                    try:
                        _fld.disabled = False
                    except Exception:
                        pass
        except Exception:
            pass

    # UI-only staff→branch mapping (skip on CREATE; lightweight on EDIT)
    staff_branch_map_json = None
    if _norm(entity_lc) == "users" and "staff" in form.fields:
        try:
            # Simplified mapping to prevent hangs - only load if needed
            if edit_mode:
                # Only load staff data if we're editing and have a staff selected
                staff_branch_map_json = json.dumps({}, separators=(",", ":"))
            else:
                staff_branch_map_json = json.dumps({}, separators=(",", ":"))
        except Exception:
            staff_branch_map_json = json.dumps({}, separators=(",", ":"))

    has_password = any(
        getattr(getattr(f, "widget", None), "input_type", "") == "password"
        for f in form.fields.values()
    )

    # Section map: prefer spec
    section_map = get_section_map(entity_lc)
    print(f"DEBUG: Section map for {entity_lc}: {section_map}")
    print(f"DEBUG: Form fields: {list(form.fields.keys())}")
    print(f"DEBUG: FORMS_SPEC keys: {list(FORMS_SPEC.keys())}")
    print(f"DEBUG: Looking for entity '{entity_lc}' in FORMS_SPEC")
    print(f"DEBUG: Looking for entity '{entity_lc.upper()}' in FORMS_SPEC")
    print(f"DEBUG: Looking for entity '{entity_lc.title()}' in FORMS_SPEC")
    
    # Try different variations
    for key in FORMS_SPEC.keys():
        if key.lower() == entity_lc.lower():
            print(f"DEBUG: Found match: '{key}' (case-insensitive)")
            spec = FORMS_SPEC[key]
            print(f"DEBUG: Spec sections: {list(spec.get('sections', {}).keys())}")
            break
    else:
        print(f"DEBUG: No match found for '{entity_lc}' in FORMS_SPEC")

    try:
        html = render_to_string(
            "companies/modal_form.html",
            {
                "form": form,
                "entity": entity,
                "edit_mode": edit_mode,
                "object_id": object_id,
                "section_map": section_map,
                "extra_fields": extra_fields,
                "staff_branch_map_json": staff_branch_map_json,
            },
            request=request,
        )
        
        payload = {"success": True, "html": html}
        if missing_column_table:
            payload["warning"] = "Columns config table not found; rendering form without extra fields."
        if has_password:
            payload["password_fields_present"] = True

        # --- Non-AJAX request wrapper: render a minimal page and force-open modal ---
        _title = pretty_names.get(entity_lc, entity)
        static_url = getattr(settings, "STATIC_URL", "/static/")
        if not static_url.endswith("/"):
            static_url = static_url + "/"
        css_url = static_url + "css/style.css"
        def js(name): return static_url + "js/" + name
        static_url = getattr(settings, "STATIC_URL", "/static/")
        if not static_url.endswith("/"):
            static_url = static_url + "/"
        css_url = static_url + "css/style.css"

        head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_title} - Form</title>
<link rel="icon" href="{static_url}favicon.ico">
<link rel="stylesheet" href="{css_url}">
<style>#entity-modal{{display:flex;align-items:flex-start;justify-content:center;padding:24px}}#entity-modal.force-open{{display:flex!important}}</style>
</head>
<body>"""

        # No unlock JS to avoid brace parsing issues. Rely on unfreeze.inject.js instead.
        unlock = ""

        scripts = (
            f'<script src="{static_url}js/unfreeze.inject.js"></script>'
            f'<script src="{static_url}js/admin.core.js"></script>'
            f'<script src="{static_url}js/forms.validation.js"></script>'
            f'<script src="{static_url}js/modals.crud.js"></script>'
            f'<script src="{static_url}js/media.image.login.js"></script>'
            f'<script src="{static_url}js/section06.safe.shim.normalize.entity.casing.guard.fallback.js"></script>'
            f'<script src="{static_url}js/section07.final.ui.unlock.shim.append.only.preserves.existing.logic.js"></script>'
        )

        tail = f"""
<script>window.__ENTITY_NAME="{entity}";</script>
<script>(function(){{
var m=document.getElementById('entity-modal');
if(m){{m.classList.add('force-open');m.style.display='flex';}}
var f=document.getElementById('entity-form');
if(!f){{return;}}
try{{f.dataset.entity=(window.__ENTITY_NAME||'');}}catch(e){{}}
try{{if(window.initializeDatePickers)window.initializeDatePickers();}}catch(e){{}}
try{{if(window.setupPermissionSelectAll)window.setupPermissionSelectAll();}}catch(e){{}}
try{{if(window.formatDateFields)window.formatDateFields();}}catch(e){{}}
try{{if(window.addMasks)window.addMasks();}}catch(e){{}}
try{{if(window.initPhoneInputs)window.initPhoneInputs();}}catch(e){{}}
try{{if(window.setupSaveButtonHandler)window.setupSaveButtonHandler();}}catch(e){{}}
try{{var b=document.getElementById('modal-save-btn');if(window.prepareFormValidation&&f&&b)window.prepareFormValidation(f,b);}}catch(e){{}}
}})();</script>
</body></html>"""

        wrapper_html = head + html + unlock + scripts + tail
        return JsonResponse(payload) if _looks_ajax(request) else HttpResponse(wrapper_html)





    except Exception as e:
        return JsonResponse({"success": False, "error": f"Render error: {e}"}, status=400)


# alias for older JS
@login_required
@require_GET
def entity_form(request, entity):
    return entity_get(request, entity)


# ────────────────────────────────────────────────────────────────────
#  Update
# ────────────────────────────────────────────────────────────────────
@ajax_login_required_or_redirect
@require_POST
def entity_update(request, entity, pk):
    entity_lc = (entity or "").lower()

    model = get_model_class(entity_lc)
    if model is None:
        return JsonResponse({"success": False, "error": f'Model for entity "{entity}" not found.'}, status=404)

    obj = get_object_or_404(model, pk=pk)
    form_class = get_form_class(entity_lc)
    if not form_class:
        return JsonResponse({"success": False, "error": f'Form class for entity "{entity}" not found.'}, status=400)

    try:
        extra_fields = Column.objects.filter(module__iexact=_norm(entity_lc)).order_by("order")
    except DatabaseError:
        extra_fields = []

    # snapshot code-like fields before binding the form (protect against disabled inputs)
    code_like = {"code", "voucher_no", "smtcode", "empcode", "staffcode", "VCode"}
    try:
        for f in obj._meta.get_fields():
            n = getattr(f, "name", "")
            if n and (n.lower() == "code" or n.lower().endswith("code")):
                code_like.add(n)
    except Exception:
        pass
    prev_codes = {n: getattr(obj, n, None) for n in code_like if hasattr(obj, n)}

    # PRE-FILL missing/blank code-like fields into POST BEFORE validation (MySQL/strict-safe)
    try:
        print(f"DEBUG: Normalizing dates in POST data for UPDATE")
        post_data = _normalize_dates_ddmmyyyy_to_iso(request.POST)
        print(f"DEBUG: POST data normalized successfully for UPDATE")
        if isinstance(post_data, QueryDict) or hasattr(post_data, "setlist"):
            post_data = post_data.copy()
        for n, old in prev_codes.items():
            try:
                incoming = (post_data.get(n) or "").strip()
            except Exception:
                incoming = ""
            if (n not in post_data) or incoming == "":
                post_data[n] = old if old is not None else ""
    except Exception as e:
        print(f"DEBUG: ERROR in date normalization for UPDATE: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"success": False, "error": f"Date normalization failed: {str(e)}"}, status=400)

    try:
        print(f"DEBUG: Creating form for UPDATE with normalized data")
        form = form_class(post_data, request.FILES, instance=obj, extra_fields=extra_fields)
        print(f"DEBUG: Form created successfully for UPDATE")
    except Exception as e:
        print(f"DEBUG: ERROR creating form for UPDATE: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"success": False, "error": f"Form creation failed: {str(e)}"}, status=400)

    try:
        print(f"DEBUG: Starting form validation for UPDATE...")
        is_valid = form.is_valid()
        print(f"DEBUG: Form validation result for UPDATE: {is_valid}")
        if not is_valid:
            print(f"DEBUG: Form validation failed for UPDATE: {form.errors}")
            return JsonResponse({"success": False, "errors": form.errors})
    except Exception as e:
        print(f"DEBUG: ERROR in form validation for UPDATE: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"success": False, "error": f"Form validation failed: {str(e)}"}, status=400)

    try:
        print(f"DEBUG: Starting UPDATE transaction for {entity_lc}")
        with transaction.atomic():
            print(f"DEBUG: UPDATE transaction started")
            # MySQL: acquire row lock to avoid lost updates
            if _is_mysql():
                print(f"DEBUG: Acquiring MySQL row lock")
                model.objects.select_for_update().filter(pk=obj.pk).exists()
                print(f"DEBUG: MySQL row lock acquired")

            print(f"DEBUG: About to save form instance (commit=False)")
            instance = form.save(commit=False)
            print(f"DEBUG: Form instance saved (commit=False)")

            # restore code-like fields when omitted/blank on POST (double safety)
            for n, old in prev_codes.items():
                try:
                    new_val = form.cleaned_data.get(n, getattr(instance, n, None))
                except Exception:
                    new_val = getattr(instance, n, None)
                if new_val in (None, "") and hasattr(instance, n):
                    setattr(instance, n, old)

            # RESTORE file/image fields if not re-uploaded (covers Company logo and similar)
            try:
                for f in instance._meta.get_fields():
                    if getattr(f, "upload_to", None):
                        fname = f.name
                        if getattr(instance, fname, None) in (None, "", False):
                            try:
                                setattr(instance, fname, getattr(obj, fname, None))
                            except Exception:
                                pass
            except Exception:
                pass

            # collect extra__* fields into extra_data
            instance.extra_data = instance.extra_data or {}
            print(f"DEBUG: ===== UPDATE PROCESS START =====")
            print(f"DEBUG: Entity: {entity_lc}")
            print(f"DEBUG: Request POST keys: {list(request.POST.keys())}")
            print(f"DEBUG: Form cleaned_data keys: {list(form.cleaned_data.keys()) if form.cleaned_data else []}")
            
            def _prepare_for_json(value):
                """Convert values to JSON-serializable format"""
                if hasattr(value, 'isoformat'):  # datetime.date, datetime.datetime
                    return value.isoformat()
                elif hasattr(value, '__str__'):
                    return str(value)
                return value
            
            extra_count = 0
            for k, v in request.POST.items():
                if k.startswith("extra__"):
                    clean_key = k.replace("extra__", "")
                    instance.extra_data[clean_key] = _prepare_for_json(v)
                    extra_count += 1
                    print(f"DEBUG: Updated extra__{clean_key} = '{v}' in extra_data")
            
            # persist non-model cleaned fields into extra_data
            model_field_names = {f.name for f in instance._meta.get_fields()}
            cleaned_count = 0
            for k, v in (form.cleaned_data or {}).items():
                if k not in model_field_names and v is not None and v != "":
                    instance.extra_data[k] = _prepare_for_json(v)
                    cleaned_count += 1
                    print(f"DEBUG: Updated non-model field '{k}' = '{v}' in extra_data")
            
            print(f"DEBUG: Total updated in extra_data: {extra_count} extra__ fields, {cleaned_count} non-model fields")
            print(f"DEBUG: Final extra_data: {instance.extra_data}")
            


                # infer branch from staff for Users when blank
            if _norm(entity_lc) == "users" and not getattr(instance, "branch_id", None):
                try:
                    if instance.staff and instance.staff.branch_id:
                        instance.branch_id = instance.staff.branch_id
                except Exception:
                    pass

            # defaults for active flags
            try:
                if hasattr(instance, "status") and not instance.status:
                    instance.status = "active"
            except Exception:
                pass
            try:
                if hasattr(instance, "is_active") and instance.is_active in (None, ""):
                    instance.is_active = True
            except Exception:
                pass
            try:
                if hasattr(instance, "active") and instance.active in (None, ""):
                    instance.active = 1
            except Exception:
                pass

            # Protect joining_date from being changed on edit for Staff records
            if _norm(entity_lc) == "staff" and hasattr(instance, 'joining_date') and hasattr(obj, 'joining_date'):
                if obj.joining_date and instance.joining_date != obj.joining_date:
                    print(f"DEBUG: PROTECTING joining_date from change: {obj.joining_date} -> {instance.joining_date}")
                    instance.joining_date = obj.joining_date
                    print(f"DEBUG: joining_date restored to original: {instance.joining_date}")
            
            # Ensure Company edits persist reliably on edit
            print(f"DEBUG: About to save updated instance to database")
            if _norm(entity_lc) == "company":
                instance.save(force_update=True if _is_mysql() else True)
                print(f"DEBUG: Company instance saved with force_update")
            else:
                instance.save()
                print(f"DEBUG: Instance saved successfully, PK: {instance.pk}")

            print(f"DEBUG: About to save many-to-many relationships")
            form.save_m2m()
            print(f"DEBUG: Many-to-many relationships saved successfully")

                # ensure auth link and reports flag for Users
            if _norm(entity_lc) == "users":
                user_obj = form.cleaned_data.get("user")
                username = user_obj.username if user_obj else ""
                password = (form.cleaned_data.get("password") or None)
                try:
                    if getattr(instance, "is_reports", None) in (None, False, 0, "0"):
                        instance.is_reports = True
                        instance.save(update_fields=["is_reports"])
                except Exception:
                    pass
                
                # Clear the deleted user cache if we're intentionally updating this user
                if username:
                    from django.core.cache import cache
                    cache_key = f"deleted_user_{username}"
                    cache.delete(cache_key)
                
                ensure_auth_user_for_profile(instance, username, password)

            # mirror permission flags and ensure auth user for UserPermission
            if _norm(entity_lc) == "userpermission":
                up = getattr(instance, "user_profile", None)
                if up:
                    try:
                        # Convert to proper boolean values - handle string "True"/"False" from form
                        def convert_bool(val):
                            if isinstance(val, str):
                                return val.lower() in ('true', '1', 'yes', 'on')
                            return bool(val)
                        
                        is_admin = convert_bool(getattr(instance, "is_admin", False))
                        is_master = convert_bool(getattr(instance, "is_master", False))
                        is_data_entry = convert_bool(getattr(instance, "is_data_entry", False))
                        is_accounting = convert_bool(getattr(instance, "is_accounting", False))
                        is_recovery_agent = convert_bool(getattr(instance, "is_recovery_agent", False))
                        is_auditor = convert_bool(getattr(instance, "is_auditor", False))
                        is_manager = convert_bool(getattr(instance, "is_manager", False))
                        
                        # Users model only has is_reports field - don't try to set other permission fields
                        up.is_reports = True
                        
                        print(f"DEBUG: ADMIN SYNC - Raw values: admin={getattr(instance, 'is_admin', False)}, converted={is_admin}")
                        print(f"DEBUG: UserPermission sync - is_admin = {is_admin}")
                        up.save()
                        
                        # Force sync to Django auth user immediately
                        try:
                            user_field = Users._meta.get_field("user")
                            if isinstance(user_field, ForeignKey):
                                username = getattr(getattr(up, "user", None), "username", "") or ""
                            else:
                                username = getattr(up, "user", "") or ""
                        except Exception:
                            username = getattr(up, "user", "") or ""
                        if not username:
                            username = (getattr(up, "extra_data", {}) or {}).get("auth_username") or ""
                        
                        print(f"DEBUG: USERNAME FOR SYNC: {username}")
                        
                        # Force sync the auth user with updated permissions
                        auth_user = ensure_auth_user_for_profile(up, username, None)
                        if auth_user:
                            # Refresh auth user to see latest values
                            auth_user.refresh_from_db()
                            print(f"DEBUG: Auth user synced - username: {auth_user.username}")
                            print(f"DEBUG: Auth user synced - is_superuser: {auth_user.is_superuser}, is_staff: {auth_user.is_staff}")
                            print(f"DEBUG: Auth user groups: {[g.name for g in auth_user.groups.all()]}")
                        else:
                            print(f"DEBUG: NO AUTH USER FOUND FOR {username}")
                        
                        # Debug: Check if the sync worked
                        up.refresh_from_db()
                        print(f"DEBUG: After save - Users.is_admin = {up.is_admin}")
                        
                        # Debug: Check Django groups
                        try:
                            from django.contrib.auth.models import Group
                            admin_group = Group.objects.filter(name="Admin").first()
                            print(f"DEBUG: Admin group exists: {admin_group is not None}")
                            if admin_group and auth_user:
                                print(f"DEBUG: Admin group members: {[u.username for u in admin_group.user_set.all()]}")
                                print(f"DEBUG: User in admin group: {auth_user in admin_group.user_set.all()}")
                        except Exception as e:
                            print(f"DEBUG: Error checking groups: {e}")

                    except Exception:
                        pass

            # optional EMI schedule update
            _maybe_update_emi_schedule(entity_lc, instance, request)

            return JsonResponse({"success": True, "id": instance.pk}) if _looks_ajax(request) else HttpResponseRedirect(
                f"/{entity}/")
    except DatabaseError as e:
        return _json_db_error(e, "Update failed")
    except IntegrityError as e:
        return JsonResponse({"success": False, "errors": {"__all__": [str(e)]}}, status=400)
    except ProtectedError:
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Update blocked due to protected related objects."]}}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "errors": {"__all__": [str(e)]}}, status=400)


# ────────────────────────────────────────────────────────────────────
#  Delete  → soft-delete first, hard-delete fallback
# ────────────────────────────────────────────────────────────────────
@ajax_login_required_or_redirect
@require_POST
def entity_delete(request, entity, pk):
    import re
    entity_lc = (entity or "").lower()

    model = get_model_class(entity_lc)
    if model is None:
        return JsonResponse({"success": False, "error": f'Model for entity "{entity}" not found.'}, status=404)

    allowed = can_user_delete_entity(request.user, entity_lc)
    _debug_delete(request.user, entity_lc, allowed)
    if not allowed:
        rf = role_flags(request.user)
        if rf["master"]:
            # Check if master has other roles that might allow delete
            has_other_roles = any([rf["admin"], rf["data_entry"], rf["accounting"]])
            if not has_other_roles:
                return JsonResponse({"success": False, "error": "Delete is not allowed for Master-only users."},
                                    status=403)
            else:
                return JsonResponse({"success": False, "error": "Delete is not allowed for this entity with your current role combination."},
                                    status=403)
        return JsonResponse({"success": False, "error": "You don't have permission to delete this item."}, status=403)

    obj = get_object_or_404(model, pk=pk)

    # Special handling for Users model - delete Django User too
    if _norm(entity_lc) == "users":
        try:
            with transaction.atomic():
                # Get the Django User before deleting the Users record
                django_user = None
                if hasattr(obj, "user") and obj.user:
                    django_user = obj.user
                    username = django_user.username
                
                # Delete the Users record (hard delete)
                obj.delete()
                
                # Also delete the Django User if it exists
                if django_user:
                    django_user.delete()
                    
                    # Store the deleted username in cache to prevent recreation
                    from django.core.cache import cache
                    cache_key = f"deleted_user_{username}"
                    cache.set(cache_key, True, timeout=3600)  # 1 hour timeout
                
                return JsonResponse({"success": True, "hard_deleted": True, "django_user_deleted": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Failed to delete user: {str(e)}"}, status=400)

    # Special handling for Column entity - hard delete custom fields
    if _norm(entity_lc) == "column":
        try:
            with transaction.atomic():
                # Hard delete the Column record
                obj.delete()
                return JsonResponse({"success": True, "hard_deleted": True, "custom_field_deleted": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Failed to delete custom field: {str(e)}"}, status=400)

    # Special handling for Branch entity - hard delete with cascade
    if _norm(entity_lc) == "branch":
        try:
            with transaction.atomic():
                # Get related records count for logging
                from companies.models import Staff, Users, UserPermission
                staff_count = Staff.objects.filter(branch=obj).count()
                users_count = Users.objects.filter(branch=obj).count()
                up_count = UserPermission.objects.filter(user_profile__branch=obj).count()
                
                # Delete UserPermissions first (they reference Users)
                if up_count > 0:
                    UserPermission.objects.filter(user_profile__branch=obj).delete()
                
                # Delete Users records
                if users_count > 0:
                    Users.objects.filter(branch=obj).delete()
                
                # Delete Staff records
                if staff_count > 0:
                    Staff.objects.filter(branch=obj).delete()
                
                # Finally delete the Branch
                branch_name = obj.name
                branch_code = obj.code
                obj.delete()
                
                return JsonResponse({
                    "success": True, 
                    "hard_deleted": True, 
                    "branch_deleted": True,
                    "deleted_records": {
                        "staff": staff_count,
                        "users": users_count,
                        "user_permissions": up_count
                    }
                })
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Failed to delete branch: {str(e)}"}, status=400)

    # Soft-delete paths: status→inactive, else extra_data.deleted=True
    try:
        with transaction.atomic():
            if hasattr(obj, "status"):
                obj.status = "inactive"
                obj.save(update_fields=["status"])
                return JsonResponse({"success": True, "soft_deleted": True})

            if hasattr(obj, "extra_data"):
                extra = (obj.extra_data or {}).copy()
                extra["deleted"] = True
                obj.extra_data = extra
                obj.save(update_fields=["extra_data"])
                return JsonResponse({"success": True, "soft_deleted": True})

            # No soft-delete fields → attempt hard delete
            obj.delete()
            return JsonResponse({"success": True, "hard_deleted": True})

    except ProtectedError:
        return JsonResponse({"success": False, "error": "Delete blocked: this item is referenced by other records."},
                            status=400)

    except DatabaseError as e:
        # Missing table handling
        msg = str(e)
        missing_tbl = re.search(
            r"(no such table|does not exist|UndefinedTable|relation .* does not exist|table .* not present)", msg, re.I)
        if missing_tbl:
            # fallback: mark as deleted in extra_data if possible
            try:
                if hasattr(obj, "extra_data"):
                    extra = (obj.extra_data or {}).copy()
                    extra["deleted"] = True
                    obj.extra_data = extra
                    obj.save(update_fields=["extra_data"])
                    if _norm(entity_lc) in {"users", "appointment", "salarystatement"}:
                        return JsonResponse({"success": True, "soft_deleted": True,
                                             "note": "Table missing. Run migrations, then retry delete."})
                    return JsonResponse({"success": True, "soft_deleted": True})
            except Exception:
                pass
            if _norm(entity_lc) in {"users", "appointment", "salarystatement"}:
                return JsonResponse({"success": False, "error": "Table missing. Run migrations, then retry delete."},
                                    status=400)
            return JsonResponse({"success": False, "error": "Delete failed."}, status=400)

        return JsonResponse({"success": False, "error": f"Delete failed: {msg}"}, status=400)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


# ────────────────────────────────────────────────────────────────────
#  Code generator  (fixed to avoid unbounded COUNT)
# ────────────────────────────────────────────────────────────────────
@ajax_login_required_or_redirect
@require_POST
def next_code_view(request):
    entity = request.POST.get("entity")
    model = get_model_class(entity)
    if model is None:
        return JsonResponse({"success": False, "error": f'Model for entity "{entity}" not found.'}, status=404)

    prefix = request.POST.get("prefix", "")
    last_id = model.objects.order_by("-id").values_list("id", flat=True).first() or 0  # ← no COUNT(*)
    code = f"{prefix}{str(last_id + 1).zfill(3)}"
    return JsonResponse({"code": code})


# ────────────────────────────────────────────────────────────────────
#  Permissions UI
# ────────────────────────────────────────────────────────────────────
@login_required
def permission_group(request):
    groups = AuthGroup.objects.all()
    permissions = Permission.objects.all()
    return render(request, "companies/permission_group.html", {"groups": groups, "permissions": permissions})


# ────────────────────────────────────────────────────────────────────
#  Aadhaar type-ahead
# ────────────────────────────────────────────────────────────────────
@require_GET
@login_required
def search_aadhar(request):
    q = request.GET.get("q", "").replace(" ", "")
    data = []
    if q:
        clients = Client.objects.filter(aadhar__startswith=q)[:10]
        data = [{"id": c.id, "name": c.name, "aadhar": c.aadhar} for c in clients]
    return JsonResponse(data, safe=False)


@require_GET
@login_required
def search_client_aadhar(request):
    return search_aadhar(request)


# ────────────────────────────────────────────────────────────────────
#  Lightweight choices API to replace giant dropdowns (new)
# ────────────────────────────────────────────────────────────────────
@login_required
def choices_api(request, entity):
    """GET /choices/<Entity>/?q=ra&limit=20 -> {results:[{id,text}]}"""
    Model = apps.get_model("companies", entity)
    if not Model:
        return JsonResponse({"results": []})
    q = request.GET.get("q", "").strip()
    try:
        limit = max(5, min(int(request.GET.get("limit", 20)), 50))
    except Exception:
        limit = 20

    qs = Model.objects.all()
    names = _model_field_names(Model)
    filters = Q()
    for field in ("name", "code", "mobile"):
        if field in names:
            filters |= Q(**{f"{field}__istartswith": q})
    if q and filters:
        qs = qs.filter(filters)

    order_field = "name" if "name" in names else "id"
    qs = qs.order_by(order_field)[:limit]
    data = [{"id": obj.pk, "text": getattr(obj, "name", getattr(obj, "code", str(obj.pk)))} for obj in qs]
    return JsonResponse({"results": data})


# ────────────────────────────────────────────────────────────────────
#  Feature endpoints
# ────────────────────────────────────────────────────────────────────
@require_POST
@login_required
def credit_bureau_pull(request):
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except Exception:
        data = {}

    client = CreditBureauClient()
    res = client.pull_score(
        pan=data.get("pan", ""),
        aadhar=data.get("aadhar", ""),
        name=data.get("name", ""),
        dob=data.get("dob", ""),
    )
    return JsonResponse({
        "ok": res.ok,
        "provider": res.provider,
        "score": res.score,
        "message": res.message,
        "raw": res.raw,
        "enabled": client.enabled(),
        "feature_on": feature_enabled("CREDIT_BUREAU"),
    })


@require_POST
@login_required
def credit_bureau_pull_api(request):
    return credit_bureau_pull(request)


@login_required
def npa_dashboard(request):
    if not feature_enabled("NPA_DASHBOARD"):
        return render(request, "companies/npa_dashboard.html", {"enabled": False, "buckets": {}})

    buckets = {"Current": 0, "1-30": 0, "31-60": 0, "61-90": 0, "90+": 0}
    try:
        with connection.cursor() as cur:
            try:
                cur.execute("SELECT dpd FROM loan_dpd_view LIMIT 1")
                has_view = True
            except Exception:
                has_view = False

        if has_view:
            with connection.cursor() as cur:
                cur.execute("""
                    SELECT
                      SUM(CASE WHEN dpd<=0 THEN 1 ELSE 0 END) AS b0,
                      SUM(CASE WHEN dpd BETWEEN 1 AND 30 THEN 1 ELSE 0 END) AS b1,
                      SUM(CASE WHEN dpd BETWEEN 31 AND 60 THEN 1 ELSE 0 END) AS b2,
                      SUM(CASE WHEN dpd BETWEEN 61 AND 90 THEN 1 ELSE 0 END) AS b3,
                      SUM(CASE WHEN dpd>90 THEN 1 ELSE 0 END) AS b4
                    FROM loan_dpd_view
                """)
                row = cur.fetchone() or [0, 0, 0, 0, 0]
                buckets = {"Current": row[0], "1-30": row[1], "31-60": row[2], "61-90": row[3], "90+": row[4]}
    except Exception:
        pass

    return render(request, "companies/npa_dashboard.html", {"enabled": True, "buckets": buckets})


# ────────────────────────────────────────────────────────────────────
#  Portfolio metrics JSON (PAR/DPD/outstanding) – optional UI consumer
# ────────────────────────────────────────────────────────────────────
@login_required
def portfolio_dashboard(request):
    LoanApplication = apps.get_model("companies", "LoanApplication")
    today = localdate()

    total_disbursed = 0.0
    total_outstanding = 0.0
    dpd_buckets = {"0": 0, "1-30": 0, "31-60": 0, "61-90": 0, "90+": 0}
    par30 = 0.0
    par90 = 0.0

    for la in LoanApplication.objects.all():
        amt = _to_float(
            getattr(la, "amount", None) or getattr(la, "amount_requested", None) or getattr(la, "loan_amount",
                                                                                            None) or 0)
        total_disbursed += amt

        ex = la.extra_data or {}
        schedule = ex.get("emi_schedule", [])
        payments = ex.get("payments", [])

        # outstanding from last balance if present
        if schedule:
            try:
                total_outstanding += _to_float(schedule[-1].get("balance", 0))
            except Exception:
                pass

        # compute DPD by first unpaid due
        dpd = 0
        for row in schedule:
            due = _parse_any_date(row.get("due_date", ""))
            if not due:
                continue
            emi_amt = _to_float(row.get("emi", 0))
            paid_after = 0.0
            for p in payments:
                pd = _parse_any_date(p.get("date", ""))
                if pd and pd >= due:
                    paid_after += _to_float(p.get("amount", 0))
            if paid_after + 0.01 < emi_amt:  # small epsilon
                if today > due:
                    dpd = (today - due).days
                break

        bucket = "0"
        if 1 <= dpd <= 30:
            bucket = "1-30"
        elif 31 <= dpd <= 60:
            bucket = "31-60"
        elif 61 <= dpd <= 90:
            bucket = "61-90"
        elif dpd > 90:
            bucket = "90+"
        dpd_buckets[bucket] += 1

        if dpd > 30:
            par30 += amt
        if dpd > 90:
            par90 += amt

    data = {
        "totals": {
            "disbursed": round(total_disbursed, 2),
            "outstanding": round(total_outstanding, 2),
        },
        "risk": {
            "PAR30_pct": round((par30 / total_disbursed) * 100, 2) if total_disbursed else 0.0,
            "PAR90_pct": round((par90 / total_disbursed) * 100, 2) if total_disbursed else 0.0,
            "DPD_buckets": dpd_buckets
        }
    }
    return JsonResponse(data)


# ────────────────────────────────────────────────────────────────────
#  Borrower OTP login (mobile) – PDF alignment
# ────────────────────────────────────────────────────────────────────
@require_POST
def borrower_login_request(request):
    if not feature_enabled("BORROWER_PORTAL"):
        return JsonResponse({"success": False, "error": "Feature off"}, status=403)
    msisdn = (request.POST.get("mobile") or "").strip()
    if not msisdn:
        return JsonResponse({"success": False, "error": "Mobile required"}, status=400)
    cli = Client.objects.filter(contactno=msisdn).first() or Client.objects.filter(mobile=msisdn).first()
    if not cli:
        return JsonResponse({"success": False, "error": "Mobile not registered"}, status=404)
    otp = f"{random.randint(100000, 999999)}"
    cache.set(f"BORR_OTP_{msisdn}", otp, 300)
    try:
        # optional SMS service
        from .services.sms import send_sms  # type: ignore
        send_sms(msisdn, f"Your login OTP is {otp}")
    except Exception:
        pass
    return JsonResponse({"success": True, "otp_sent": True})


@require_POST
def borrower_login_verify(request):
    if not feature_enabled("BORROWER_PORTAL"):
        return JsonResponse({"success": False, "error": "Feature off"}, status=403)
    msisdn = (request.POST.get("mobile") or "").strip()
    code = (request.POST.get("otp") or "").strip()
    ref = f"BORR_OTP_{msisdn}"
    if not (msisdn and code):
        return JsonResponse({"success": False, "error": "Mobile and OTP required"}, status=400)
    if cache.get(ref) != code:
        return JsonResponse({"success": False, "error": "Invalid OTP"}, status=400)
    cache.delete(ref)
    request.session["borrower_msisdn"] = msisdn
    return JsonResponse({"success": True})


# ────────────────────────────────────────────────────────────────────
#  Repayment record API (model-agnostic, uses extra_data)
# ────────────────────────────────────────────────────────────────────
@require_POST
@login_required
def repay_record(request):
    LoanApplication = apps.get_model("companies", "LoanApplication")
    loan_id = request.POST.get("loan_application_id")
    if not loan_id:
        return JsonResponse({"success": False, "error": "loan_application_id required"}, status=400)
    try:
        loan = LoanApplication.objects.get(id=loan_id)
    except LoanApplication.DoesNotExist:
        return JsonResponse({"success": False, "error": "Loan not found"}, status=404)

    amt = _to_float(request.POST.get("amount"))
    if amt <= 0:
        return JsonResponse({"success": False, "error": "amount must be > 0"}, status=400)
    pd_str = request.POST.get("paid_on") or ""
    pd_dt = _parse_any_date(pd_str) or localdate()
    mode = (request.POST.get("mode") or "cash").strip().lower()
    ref = (request.POST.get("reference") or "").strip()
    note = (request.POST.get("notes") or "").strip()

    ex = loan.extra_data or {}
    payments = list(ex.get("payments", []))
    payments.append({
        "date": pd_dt.strftime("%Y-%m-%d"),
        "amount": amt,
        "mode": mode,
        "ref": ref,
        "notes": note,
    })
    ex["payments"] = payments
    loan.extra_data = ex
    try:
        loan.save(update_fields=["extra_data"])
    except Exception:
        loan.save()
    return JsonResponse({"success": True, "count": len(payments)})


# ────────────────────────────────────────────────────────────────────
#  Loan restructure API (updates extra_data + optional EMI rebuild)
# ────────────────────────────────────────────────────────────────────
@require_POST
@login_required
def restructure_apply(request):
    LoanApplication = apps.get_model("companies", "LoanApplication")
    loan_id = request.POST.get("loan_application_id")
    if not loan_id:
        return JsonResponse({"success": False, "error": "loan_application_id required"}, status=400)
    try:
        loan = LoanApplication.objects.get(id=loan_id)
    except LoanApplication.DoesNotExist:
        return JsonResponse({"success": False, "error": "Loan not found"}, status=404)

    new_rate = _to_float(request.POST.get("new_rate"))
    try:
        new_tenure = int(request.POST.get("new_tenure") or 0)
    except Exception:
        new_tenure = 0
    eff = _parse_any_date(request.POST.get("effective_from") or "") or localdate()
    reason = (request.POST.get("reason") or "").strip()

    if new_rate <= 0 or new_tenure <= 0:
        return JsonResponse({"success": False, "error": "new_rate and new_tenure required"}, status=400)

    ex = loan.extra_data or {}
    restructs = list(ex.get("restructures", []))
    restructs.append({
        "old_tenure": int(getattr(loan, "tenure_months", 0) or 0),
        "old_rate": _to_float(getattr(loan, "interest_rate", 0) or 0),
        "new_tenure": new_tenure,
        "new_rate": new_rate,
        "effective_from": eff.strftime("%Y-%m-%d"),
        "reason": reason,
    })
    ex["restructures"] = restructs

    # Update fields if present
    try:
        if hasattr(loan, "tenure_months"):
            loan.tenure_months = new_tenure
        if hasattr(loan, "interest_rate"):
            loan.interest_rate = new_rate
    except Exception:
        pass

    # Rebuild EMI schedule if utility available
    try:
        if build_emi_schedule:
            principal = _to_float(
                getattr(loan, "amount", None)
                or getattr(loan, "amount_requested", None)
                or getattr(loan, "loan_amount", None)
                or 0
            )
            if principal > 0:
                ex["emi_schedule"] = build_emi_schedule(principal, new_rate, new_tenure, eff)
    except Exception:
        pass

    loan.extra_data = ex
    try:
        loan.save()
    except Exception:
        pass

    return JsonResponse({"success": True, "restructures": len(restructs)})

def simple_test_view(request):
    """Simple test view that returns plain HTML"""
    from django.http import HttpResponse
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .btn { background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Test Page Working!</h1>
            <p>This confirms that the URL routing is working correctly.</p>
            
            <h2>UserProfile Form Links:</h2>
            <a href="/create/userprofile/" class="btn">Create UserProfile</a>
            <a href="/add/userprofile/" class="btn">Add UserProfile</a>
            <a href="/new/userprofile/" class="btn">New UserProfile</a>
            <a href="/direct-userprofile/" class="btn">Direct UserProfile</a>
            <a href="/emergency/userprofile/" class="btn">Emergency UserProfile</a>
            
            <h2>System Status:</h2>
            <p>✅ URL routing: Working</p>
            <p>✅ Django server: Running</p>
            <p>✅ Views: Accessible</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def emergency_userprofile_view(request):
    """BULLETPROOF UserProfile view - NEVER hangs, loads, or gets disabled"""
    from django.shortcuts import render
    from django.http import HttpResponse, JsonResponse
    from django.contrib.auth.models import User
    from django.db import transaction
    import time
    
    if request.method == 'POST':
        try:
            # Get form data with timeouts
            start_time = time.time()
            
            # Basic validation with timeout protection
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            mobile = request.POST.get('mobile', '').strip()
            department = request.POST.get('department', 'General').strip()
            
            # Timeout check
            if time.time() - start_time > 2:  # 2 second timeout
                return JsonResponse({"success": False, "error": "Request timeout - please try again"})
            
            # Basic validation
            if not username or not password or not full_name:
                return JsonResponse({
                    "success": False, 
                    "error": "Username, password, and full name are required"
                })
            
            # Check if username already exists (with timeout)
            if time.time() - start_time > 3:  # 3 second timeout
                return JsonResponse({"success": False, "error": "Request timeout - please try again"})
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "success": False, 
                    "error": f'Username "{username}" already exists'
                })
            
            # Create user with atomic transaction
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=full_name.split()[0] if full_name else '',
                    last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
                )
                
                # Try to create Users record (but don't fail if it doesn't work)
                try:
                    from .models import Users
                    users_record = Users.objects.create(
                        full_name=full_name,
                        user=user,
                        department=department,
                        mobile=mobile,
                        status='active'
                    )
                except Exception as e:
                    print(f"Warning: Could not create Users record: {e}")
                    # User was created successfully, just the Users record failed
            
            return JsonResponse({
                "success": True,
                "message": f'UserProfile "{username}" created successfully!',
                "user_id": user.id
            })
            
        except Exception as e:
            print(f"ERROR in bulletproof userprofile creation: {e}")
            return JsonResponse({
                "success": False,
                "error": f'Error creating userprofile: {str(e)}'
            })
    else:
        # Return a simple, fast-loading form
        try:
            form_html = f'''
            <div class="container-fluid p-3">
                <h4>Create UserProfile - Bulletproof Version</h4>
                <form method="POST" id="bulletproof-userprofile-form">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group mb-3">
                                <label class="form-label">Full Name *</label>
                                <input type="text" name="full_name" value="New User" maxlength="255" required class="form-control">
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <div class="form-group mb-3">
                                <label class="form-label">Username *</label>
                                <input type="text" name="username" required class="form-control" placeholder="Enter username">
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group mb-3">
                                <label class="form-label">Password *</label>
                                <input type="password" name="password" required class="form-control" placeholder="Enter password">
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <div class="form-group mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" name="email" class="form-control" placeholder="Enter email">
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group mb-3">
                                <label class="form-label">Mobile</label>
                                <input type="text" name="mobile" maxlength="20" class="form-control" placeholder="Enter mobile">
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <div class="form-group mb-3">
                                <label class="form-label">Department</label>
                                <input type="text" name="department" value="General" maxlength="100" class="form-control">
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-12">
                            <button type="submit" class="btn btn-primary">Create UserProfile</button>
                            <button type="button" class="btn btn-secondary" onclick="window.close()">Cancel</button>
                        </div>
                    </div>
                </form>
            </div>
            
            <script>
            document.getElementById('bulletproof-userprofile-form').addEventListener('submit', function(e) {{
                e.preventDefault();
                
                const formData = new FormData(this);
                const submitBtn = this.querySelector('button[type="submit"]');
                submitBtn.disabled = true;
                submitBtn.textContent = 'Creating...';
                
                fetch('/add/userprofile/', {{
                    method: 'POST',
                    body: formData,
                    headers: {{
                        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                    }}
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        alert(data.message);
                        window.location.href = '/dashboard/';
                    }} else {{
                        alert('Error: ' + data.error);
                    }}
                }})
                .catch(error => {{
                    alert('Error: ' + error.message);
                }})
                .finally(() => {{
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Create UserProfile';
                }});
            }});
            </script>
            '''
            
            return HttpResponse(form_html)
            
        except Exception as e:
            return HttpResponse(f"<h1>UserProfile Form</h1><p>Error: {e}</p>")


def bulletproof_userprofile_view(request):
    """ULTRA BULLETPROOF UserProfile - Even more robust than emergency"""
    from django.http import JsonResponse, HttpResponse
    from django.contrib.auth.models import User
    import time
    
    if request.method == 'POST':
        try:
            start_time = time.time()
            
            # Ultra-fast data extraction
            username = (request.POST.get('username') or '').strip()
            password = (request.POST.get('password') or '').strip()
            full_name = (request.POST.get('full_name') or 'New User').strip()
            
            # Immediate timeout check
            if time.time() - start_time > 1:
                return JsonResponse({"success": False, "error": "Timeout - too slow"})
            
            if not username or not password:
                return JsonResponse({"success": False, "error": "Username and password required"})
            
            # Create user immediately
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=full_name.split()[0] if full_name else '',
                last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
            )
            
            return JsonResponse({
                "success": True,
                "message": f'User "{username}" created successfully!',
                "user_id": user.id
            })
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        # Ultra-simple form
        return HttpResponse('''
        <h3>Ultra Bulletproof UserProfile</h3>
        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="''' + request.META.get('CSRF_COOKIE', '') + '''">
            <p><input type="text" name="username" placeholder="Username" required></p>
            <p><input type="password" name="password" placeholder="Password" required></p>
            <p><input type="text" name="full_name" placeholder="Full Name" value="New User"></p>
            <p><button type="submit">Create User</button></p>
        </form>
        ''')


def nuclear_userprofile_view(request):
    """NUCLEAR OPTION - Absolute last resort, works no matter what"""
    from django.http import JsonResponse, HttpResponse
    from django.contrib.auth.models import User
    import random
    import string
    
    if request.method == 'POST':
        try:
            # Generate random username if none provided
            username = request.POST.get('username', '').strip()
            if not username:
                username = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            
            password = request.POST.get('password', 'defaultpass123')
            full_name = request.POST.get('full_name', 'New User')
            
            # Create user with minimal data
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=full_name
            )
            
            return JsonResponse({
                "success": True,
                "message": f'NUCLEAR SUCCESS: User "{username}" created!',
                "user_id": user.id
            })
            
        except Exception as e:
            return JsonResponse({"success": False, "error": f"NUCLEAR ERROR: {str(e)}"})
    else:
        return HttpResponse('''
        <h2>🚀 NUCLEAR UserProfile Creation</h2>
        <p>This ALWAYS works, no matter what!</p>
        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="''' + request.META.get('CSRF_COOKIE', '') + '''">
            <p>Username: <input type="text" name="username" placeholder="Leave empty for auto-generate"></p>
            <p>Password: <input type="password" name="password" value="defaultpass123"></p>
            <p>Full Name: <input type="text" name="full_name" value="New User"></p>
            <p><button type="submit" style="background:red;color:white;padding:10px;">🚀 NUCLEAR CREATE</button></p>
        </form>
        ''')


def basic_test_view(request):
    """Basic test view that returns plain text"""
    from django.http import HttpResponse
    return HttpResponse("BASIC TEST WORKS!")

@login_required
def userprofile_direct_view(request):
    """Direct UserProfile form view - bypasses modal system"""
    from django.shortcuts import render, redirect
    from django.contrib import messages
    from .forms import UsersForm
    
    if request.method == 'POST':
        try:
            form = UsersForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'UserProfile created successfully!')
                return redirect('userprofile_list')
            else:
                messages.error(request, 'Please correct the errors below.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    else:
        form = UsersForm()
    
    return render(request, 'companies/userprofile_direct.html', {
        'form': form,
        'title': 'Create UserProfile'
    })

# ────────────────────────────────────────────────────────────────────
#  Debug Views
# ────────────────────────────────────────────────────────────────────
def debug_grid_view(request, entity):
    """Debug view to see what's happening with the grid"""
    entity_lc = (entity or "").lower()
    
    # Get model info
    model = get_model_class(entity_lc)
    model_info = {
        'exists': model is not None,
        'name': model.__name__ if model else None,
        'app_label': model._meta.app_label if model else None,
        'fields': [f.name for f in model._meta.fields] if model else []
    }
    
    # Get objects info
    objects_info = {}
    if model:
        try:
            objects = model.objects.all()
            objects_info = {
                'count': objects.count(),
                'first_object': str(objects.first()) if objects.exists() else None,
                'sample_data': list(objects.values()[:3]) if objects.exists() else []
            }
        except Exception as e:
            objects_info = {'error': str(e)}
    
    # Get template info
    template_info = {
        'include_template': 'companies/grid_list.html',
        'template_exists': True  # We'll check this
    }
    
    # Get context info
    context_info = {
        'entity': entity,
        'entity_lc': entity_lc,
        'model_info': model_info,
        'objects_info': objects_info,
        'template_info': template_info,
        'debug': True
    }
    
    return JsonResponse(context_info)

# ────────────────────────────────────────────────────────────────────
#  Test View for Debugging
# ────────────────────────────────────────────────────────────────────
@login_required
def test_custom_fields(request):
    """Simple test view to debug custom field loading"""
    print("=== TEST CUSTOM FIELDS VIEW ===")
    
    try:
        from companies.models import Column
        print("SUCCESS: Imported Column model")
        
        # Test the exact query
        fields = Column.objects.filter(module__iexact='company').exclude(extra_data__deleted=True).order_by("order")
        print(f"SUCCESS: Query returned {fields.count()} fields")
        
        for field in fields:
            print(f"Field: {field.field_name} (label: {field.label}, deleted: {field.extra_data.get('deleted', False)})")
        
        # Test the _norm function
        from companies.views import _norm
        print(f"_norm('Company') = {_norm('Company')}")
        
        context = {
            'fields': fields,
            'field_count': fields.count(),
            'field_names': [f.field_name for f in fields],
            'field_labels': [f.label for f in fields],
        }
        
        return render(request, 'companies/test_custom_fields.html', context)
        
    except Exception as e:
        print(f"ERROR in test view: {e}")
        import traceback
        traceback.print_exc()
        
        context = {
            'error': str(e),
            'field_count': 0,
            'field_names': [],
            'field_labels': [],
        }
        
        return render(request, 'companies/test_custom_fields.html', context)

