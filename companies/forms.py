# forms.py
from django import forms
from django.forms import TextInput, ClearableFileInput
from django.utils.timezone import localdate
from django.utils import timezone
from django.db import models
from django.db.models import ForeignKey

# ── optional spec import; safe no-op if missing ──
try:
    from .forms_spec import FORMS_SPEC
except Exception:
    FORMS_SPEC = {}

from .models import (
    # core
    Company, Branch, Village, Center, Group, Role, Staff,
    Product, Client, LoanApplication, LoanApproval, Disbursement,
    BusinessSetting, FieldSchedule, FieldReport, WeeklyReport, MonthlyReport, Column, Cadre,
    # savings / mortgage (added)
    Prepaid, Mortgage, ExSaving,
    # new business tables
    AccountHead, Voucher, Posting, RecoveryPosting,
    # ⇣ auto-generated CSV models stay below ⇣
    AccCashbook, AccCashbookold, AccHeads, Aadhar, Accfundloancols, Accfundloans,
    Accountmaster, Arrear, Cheque, Codes, Contacts, Dayend, Equity2,
    Equityshare31032014, Equityshare31032015, Gr, Groups, MXAgent, MXCode,
    MXMember, MXSavings, Massposting, MasterBranch, MasterCategories, MasterFs,
    MasterLoanpurposes, MasterLoantypes, MasterMonth, MasterSectors, MasterSetup,
    MasterWeeks, MXAgriment, MXLoancols, MXLoans, MXSalaries, Pdc, RptDaybook,
    Securitydeposit, Staffloans, Transefer, Cobarower, Collectionrpt, Fund,
    Loancols, Loans, Loansmfi41110, Mloanschedule, Mloancols, Mloans, Mlogin,
    Mmisc, Mrecvisit, Msetup, Msurity, MasterBusinessmode, Memberdeposits,
    Members, Memberskaikaluru, Pbdet, Rptincome, RptGrcollectionsheet,
    RptOutstanding, RptPassbook, RptPassbookcommon, RptTb, RptDisRegister,
    RptHigh, RptSavings, RptSumsheet, Savings, Setup, Setupn, Share, Share1,
    Smtavail, Temp, Users,
    # feature models (added)
    KYCDocument, AlertRule,
    # HRPM (added)
    Appointment, SalaryStatement,
    # Separated permissions entity (added)
    UserPermission,
    # validators
    phone_validator, aadhar_validator,
    # ── sync add-ons (payments, webhook, notifications, risk) ──
    Payment, GatewayEvent, Notification, EWIFlag, LoanRestructure, Repayment
)

ACTIVE_SENTINELS = ("active", "1", 1, True)
DATE_INPUT_FORMATS = ["%d/%m/%Y", "%Y-%m-%d"]


def _truthy_active(v):
    s = str(v or "").strip().lower()
    return s in {"active", "1", "true", "yes", "y", "t"}


# ─────────────────────────────────────────────────────────────────────────────
# Spec-driven modal field injector (adds extra__* fields from FORMS_SPEC)
# ─────────────────────────────────────────────────────────────────────────────
TYPE_MAP = {
    "char": forms.CharField,
    "date": forms.DateField,
    "int":  forms.IntegerField,
    "file": forms.FileField,
    "image": forms.ImageField,
}

def _pretty_label(name: str) -> str:
    return name.replace("extra__", "").replace("_", " ").strip().title()

def _inject_spec_fields(form_obj: forms.ModelForm):
    """Add fields defined in FORMS_SPEC[Entity]['sections'] if not present."""
    try:
        entity = form_obj._meta.model.__name__
    except Exception:
        return

    spec = FORMS_SPEC.get(entity) or {}
    sections = spec.get("sections") or {}
    if not sections:
        return

    injected_count = 0

    for _section, fields in sections.items():
        for f in fields:
            if isinstance(f, dict):
                fname = f.get("name")
                ftype = f.get("type", "char")
                freq  = bool(f.get("required", False))
                flabel = f.get("label") or _pretty_label(fname)
            else:
                fname = str(f)
                ftype = "char"
                freq = False
                flabel = _pretty_label(fname)

            if not fname:
                continue

            if ftype == "select":
                # Check if this is a boolean field with choices
                if fname.startswith("is_") and "choices" in f:
                    # Handle boolean select fields with choices
                    FieldCls = forms.ChoiceField
                    kwargs = {
                        "label": flabel, 
                        "required": freq,
                        "choices": f.get("choices", [["True", "Yes"], ["False", "No"]]),
                        "widget": forms.Select(attrs={"class": "form-control"})
                    }
                    print(f"DEBUG: _inject_spec_fields - Creating boolean select field: {fname} with choices: {f.get('choices')}")
                else:
                    # Handle select fields - need to determine the model and set up queryset
                    FieldCls = PermissiveModelChoiceField
                    kwargs = {"label": flabel, "required": freq}
                    
                    if fname == "staff":
                        from .models import Staff, Users
                        # First, let's see what staff exist
                        all_staff = Staff._base_manager.all()
                        active_staff = Staff._base_manager.filter(status="active")
                        staff_with_users = Users.objects.filter(staff__isnull=False).values_list('staff_id', flat=True)
                        
                        print(f"DEBUG: Total staff count: {all_staff.count()}")
                        print(f"DEBUG: Active staff count: {active_staff.count()}")
                        print(f"DEBUG: Staff with users count: {staff_with_users.count()}")
                        
                        # Filter for active staff with valid staffcode, excluding those who already have users
                        kwargs["queryset"] = Staff._base_manager.filter(
                            status="active"
                        ).exclude(
                            staffcode__isnull=True
                        ).exclude(
                            staffcode=""
                        ).exclude(
                            id__in=staff_with_users  # Exclude staff who already have user profiles
                        ).order_by("name", "staffcode")
                        print(f"DEBUG: Available staff count: {kwargs['queryset'].count()}")
                        
                        # If no staff available, show empty queryset (no fallback)
                        if kwargs['queryset'].count() == 0:
                            print("DEBUG: No staff available - showing empty dropdown")
                            kwargs["queryset"] = Staff._base_manager.none()
                        
                        # Debug: Print the actual queryset count and values
                        print(f"DEBUG: Final staff queryset count: {kwargs['queryset'].count()}")
                        try:
                            print(f"DEBUG: Final staff queryset values: {list(kwargs['queryset'].values_list('name', 'staffcode'))}")
                        except Exception as e:
                            print(f"DEBUG: Could not get queryset values: {e}")
                    elif fname == "branch":
                        from .models import Branch
                        kwargs["queryset"] = Branch._base_manager.filter(status="active").order_by("name")
                        print(f"DEBUG: Branch queryset count: {kwargs['queryset'].count()}")
                    elif fname == "user":
                        from django.contrib.auth.models import User
                        kwargs["queryset"] = User.objects.filter(is_active=True).order_by("username")
                    else:
                        # For other select fields, try to get the model from the form's model field
                        try:
                            model_field = form_obj._meta.model._meta.get_field(fname)
                            if hasattr(model_field, 'related_model'):
                                kwargs["queryset"] = model_field.related_model._base_manager.all()
                        except Exception:
                            # Fallback to empty queryset
                            kwargs["queryset"] = form_obj._meta.model._base_manager.none()
            else:
                FieldCls = TYPE_MAP.get(ftype, forms.CharField)
                kwargs = {"label": flabel, "required": freq}
                
                if ftype == "date":
                    kwargs["widget"] = TextInput(attrs={
                        "class": "date-field form-control",
                        "placeholder": "dd/mm/yyyy",
                        "data-flatpickr": "true",
                        "autocomplete": "off",
                        "pattern": r"\d{2}/\d{2}/\d{4}",
                        "maxlength": "10",
                    })
                    kwargs["input_formats"] = DATE_INPUT_FORMATS
                elif ftype in ("file", "image"):
                    kwargs["widget"] = ClearableFileInput(attrs={"class": "form-control"})
                else:
                    kwargs["widget"] = TextInput(attrs={"class": "form-control"})

            form_obj.fields[fname] = FieldCls(**kwargs)
            injected_count += 1

    # add data-required flag for injected required fields and dates
    for nm, f in form_obj.fields.items():
        if isinstance(f.widget, forms.HiddenInput):
            continue
        if getattr(f, "required", False) or isinstance(f, forms.DateField):
            f.widget.attrs.setdefault("data-required", "true")


# ── permissive: accept PKs and common alt keys (handles CSV-imported rows) ──
class PermissiveModelChoiceField(forms.ModelChoiceField):
    default_error_messages = {
        "required": "This field is required.",
        "invalid_choice": "Selected value is not available.",
    }

    def __init__(self, *args, **kwargs):
        # Remove limit_choices_to to avoid TypeError
        kwargs.pop('limit_choices_to', None)
        kwargs.pop('to_field_name', None)
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, self.queryset.model):
            return str(value.pk)
        return super().prepare_value(value)

    def _get_by_alternates(self, raw):
        # Try common non-PK identifiers used in this project
        for alt in ("staffcode", "smtcode", "code", "voucher_no", "VCode", "name"):
            if hasattr(self.queryset.model, alt):
                try:
                    return self.queryset.model._base_manager.get(**{alt: raw})
                except self.queryset.model.DoesNotExist:
                    pass
        raise self.queryset.model.DoesNotExist

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, self.queryset.model):
            return value
        # Handle case where value might be a model instance but not the exact type
        if hasattr(value, 'pk') and hasattr(value, '_meta'):
            return value
        # Ensure we have a string before calling strip()
        if value is None:
            return None
        raw = str(value).strip()
        try:
            return self.queryset.model._base_manager.get(pk=raw)
        except (ValueError, self.queryset.model.DoesNotExist):
            try:
                return self._get_by_alternates(raw)
            except self.queryset.model.DoesNotExist:
                raise forms.ValidationError(self.error_messages["invalid_choice"], code="invalid_choice")

    def validate(self, value):
        if self.required and value in self.empty_values:
            raise forms.ValidationError(self.error_messages["required"], code="required")

    def valid_value(self, value):
        if value in self.empty_values:
            return True
        if isinstance(value, self.queryset.model):
            return True
        # Handle case where value might be a model instance but not the exact type
        if hasattr(value, 'pk') and hasattr(value, '_meta'):
            return True
        # Ensure we have a string before calling strip()
        if value is None:
            return True
        raw = str(value).strip()
        try:
            self.queryset.model._base_manager.get(pk=raw)
            return True
        except self.queryset.model.DoesNotExist:
            try:
                self._get_by_alternates(raw)
                return True
            except self.queryset.model.DoesNotExist:
                return False

    def clean(self, value):
        if value in self.empty_values:
            if self.required:
                raise forms.ValidationError(self.error_messages["required"], code="required")
            return None
        return self.to_python(value)


class ExcludeRawCSVDataForm(forms.ModelForm):
    class Meta:
        exclude = ["raw_csv_data", "extra_data"]

    def __init__(self, *args, **kwargs):
        print(f"DEBUG: ===== FORM INIT START =====")
        print(f"DEBUG: ExcludeRawCSVDataForm.__init__ called for {self.__class__.__name__}")
        print(f"DEBUG: Args: {args}")
        print(f"DEBUG: Kwargs: {kwargs}")
        print(f"DEBUG: Instance: {getattr(self, 'instance', None)}")
        print(f"DEBUG: Instance PK: {getattr(getattr(self, 'instance', None), 'pk', None)}")
        print(f"DEBUG: Instance type: {type(getattr(self, 'instance', None))}")
        if getattr(self, 'instance', None):
            print(f"DEBUG: Instance extra_data: {getattr(getattr(self, 'instance', None), 'extra_data', None)}")
            print(f"DEBUG: Instance extra_data type: {type(getattr(getattr(self, 'instance', None), 'extra_data', None))}")
        
        self.extra_fields = kwargs.pop("extra_fields", [])
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "joining_date":
                today_str = localdate().strftime("%d/%m/%Y")
                if (
                    not self.data.get(name)
                    and not self.initial.get(name)
                    and not getattr(self.instance, name)
                ):
                    field.initial = today_str
                    self.initial[name] = today_str

                field.widget.attrs.update({
                    "readonly": "readonly",
                    "class": "form-control",
                    "placeholder": "dd/mm/yyyy",
                    "autocomplete": "off",
                    "style": "pointer-events: none; background-color: #e9ecef;",
                    "data-no-flatpickr": "true",
                    "pattern": r"\d{2}/\d{2}/\d{4}",
                    "maxlength": "10",
                })
                if hasattr(field, "input_formats"):
                    field.input_formats = DATE_INPUT_FORMATS

            elif name in ("adharno", "aadhar", "aadhaar"):
                field.widget.attrs.update({
                    "placeholder": "0000 0000 0000",
                    "maxlength": "14",
                    "class": "form-control aadhar-input",
                    "inputmode": "numeric",
                    "autocomplete": "off",
                    "pattern": r"\d{4}\s\d{4}\s\d{4}",
                    "title": "Enter Aadhar in 0000 0000 0000 format using only digits",
                    "oninput": "this.value=this.value.replace(/[^0-9 ]/g,'').replace(/(\\d{4})\\s?(\\d{0,4})\\s?(\\d{0,4})/, '$1 $2 $3').trim()",
                })

            elif name in ("phone", "mobile", "contact1", "housecontactno"):
                css = field.widget.attrs.get("class", "form-control")
                field.widget.attrs.update({
                    "class": f"{css} phone-input".strip(),
                    "placeholder": "10-digit number",
                    "maxlength": "10",
                    "inputmode": "numeric",
                    "autocomplete": "off",
                    "pattern": r"\d{10}",
                    "title": "Enter 10-digit phone number using only digits",
                    "oninput": "this.value=this.value.replace(/\\D/g,'')",
                })

            elif (
                name.lower() == "code"
                or name.lower().endswith("code")
                or name in ("voucher_no", "smtcode", "empcode", "staffcode", "VCode")
            ):
                css = field.widget.attrs.get("class", "form-control")
                if not self.instance.pk:
                    field.widget.attrs["class"] = f"{css} autocode".strip()
                    field.widget.attrs["readonly"] = "readonly"
                    field.widget.attrs.setdefault("placeholder", "auto")
                    field.disabled = False
                else:
                    field.widget.attrs["class"] = " ".join(
                        c for c in str(css).split() if c != "autocode"
                    ) or "form-control"
                    field.widget.attrs.pop("readonly", None)
                    field.widget.attrs.pop("disabled", None)
                    field.widget.attrs["data-force-editable"] = "1"
                    field.disabled = False

            elif isinstance(field, (forms.ImageField, forms.FileField)):
                field.widget = ClearableFileInput(attrs={"class": "form-control"})

            elif isinstance(field, forms.DateField):
                field.input_formats = DATE_INPUT_FORMATS
                field.widget = TextInput(attrs={
                    "class": "date-field form-control",
                    "placeholder": "dd/mm/yyyy",
                    "data-flatpickr": "true",
                    "autocomplete": "off",
                    "pattern": r"\d{2}/\d{2}/\d{4}",
                    "maxlength": "10",
                })

            elif not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-control")

        for name in ("status", "is_active", "active"):
            if name in self.fields:
                f = self.fields[name]
                f.required = False
                f.widget = forms.HiddenInput()
                if name == "status":
                    val = "active"
                    try:
                        for v, _ in getattr(f, "choices", []) or []:
                            if v in ACTIVE_SENTINELS:
                                val = v
                                break
                    except Exception:
                        pass
                    f.initial = val
                    self.initial.setdefault(name, val)
                else:
                    val = True if isinstance(f, forms.BooleanField) else "1"
                    f.initial = val
                    self.initial.setdefault(name, val)

        # Dynamic Column module extra fields
        for col in self.extra_fields:
            field_kwargs = {
                "label": col.label,
                "required": col.required,
                "widget": TextInput(attrs={"class": "form-control"}),
            }

            if col.field_type == "date":
                field_cls = forms.DateField
                field_kwargs["widget"] = TextInput(attrs={
                    "class": "date-field form-control",
                    "placeholder": "dd/mm/yyyy",
                    "data-flatpickr": "true",
                    "autocomplete": "off",
                    "pattern": r"\d{2}/\d{2}/\d{4}",
                    "maxlength": "10",
                })
                field_kwargs["input_formats"] = DATE_INPUT_FORMATS

            elif col.field_type == "number":
                field_cls = forms.DecimalField

            elif col.field_type == "file":
                field_cls = forms.FileField
                field_kwargs["widget"] = ClearableFileInput(attrs={"class": "form-control"})

            else:
                field_cls = forms.CharField

            self.fields[f"extra__{col.field_name}"] = field_cls(**field_kwargs)

        _inject_spec_fields(self)

        # Automatically convert foreign key fields to dropdowns
        self._convert_foreign_keys_to_dropdowns()

        for nm, f in self.fields.items():
            if not isinstance(f.widget, forms.HiddenInput):
                if getattr(f, "required", False) or isinstance(f, forms.DateField):
                    f.widget.attrs.setdefault("data-required", "true")

        # Prefill ALL fields from instance.extra_data on EDIT (comprehensive)
        # Initialize all_form_fields at the beginning to avoid UnboundLocalError
        all_form_fields = list(self.fields.keys())
        
        try:
            instance = getattr(self, "instance", None)
            if instance and getattr(instance, "pk", None):
                model_field_names = {getattr(ff, "name", "") for ff in instance._meta.get_fields()}
                extra = (getattr(instance, "extra_data", {}) or {}).copy()

                def _fmt_date(val):
                    try:
                        s = str(val or "")
                        # If ISO YYYY-MM-DD, convert to dd/mm/YYYY for display
                        if len(s) == 10 and s[4] == '-' and s[7] == '-':
                            y, m, d = s.split('-')
                            return f"{d}/{m}/{y}"
                        # If it's already in dd/mm/yyyy format, return as is
                        elif len(s) == 10 and s[2] == '/' and s[5] == '/':
                            return val
                        return val
                    except Exception:
                        return val

                # Show all available form fields for debugging
                print(f"DEBUG: Prefilling form with {len(all_form_fields)} fields")
                print(f"DEBUG: Extra data keys: {list(extra.keys())}")
                print(f"DEBUG: Extra data values: {list(extra.values())}")
                print(f"DEBUG: Prefilling form for {instance._meta.model.__name__}")
                print(f"DEBUG: Available fields: {all_form_fields}")
                print(f"DEBUG: Extra data keys: {list(extra.keys())}")
                print(f"DEBUG: Extra data values: {extra}")

                for fname in all_form_fields:
                    # Skip if already has data from POST (but allow overriding initial)
                    if hasattr(self, 'data') and self.data and fname in self.data:
                        continue
                    
                    # Try multiple key variations for this field
                    possible_keys = []
                    if fname.startswith("extra__"):
                        clean_name = fname.replace("extra__", "", 1)
                        possible_keys.extend([clean_name, fname])
                    else:
                        possible_keys.extend([fname, f"extra__{fname}"])
                    
                    # Find the value in extra_data
                    val = None
                    found_key = None
                    for key in possible_keys:
                        if key in extra:
                            val = extra[key]
                            found_key = key
                            break
                    
                    print(f"DEBUG: Field '{fname}' - possible keys: {possible_keys}, found value: {val}, found key: {found_key}")
                    
                    if val is not None and val != "":
                        val = _fmt_date(val)
                        print(f"DEBUG: Setting initial for '{fname}' = '{val}'")
                        
                        # Set the initial value for the form
                        self.initial[fname] = val
                        
                        # For extra__ fields, we need special handling
                        if fname.startswith("extra__"):
                            try:
                                field = self.fields[fname]
                                # Set the field's initial value
                                field.initial = val
                                print(f"DEBUG: Set field.initial for '{fname}' = '{val}'")
                                
                                # For text inputs, set the widget value attribute
                                if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                                    if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.Textarea)):
                                        field.widget.attrs['value'] = val
                                        print(f"DEBUG: Set widget value for '{fname}' = '{val}'")
                                    
                                    # For select fields, set the selected option
                                    elif isinstance(field.widget, forms.Select):
                                        field.widget.attrs['data-selected'] = val
                                        print(f"DEBUG: Set data-selected for '{fname}' = '{val}'")
                                    
                                    # For date fields, format and set value
                                    elif isinstance(field.widget, forms.DateInput):
                                        field.widget.attrs['value'] = val
                                        print(f"DEBUG: Set date widget value for '{fname}' = '{val}'")
                                
                                # Also set the field's bound data
                                if hasattr(field, 'bound_data'):
                                    field.bound_data = val
                                    print(f"DEBUG: Set bound_data for '{fname}' = '{val}'")
                                    
                            except Exception as e:
                                print(f"DEBUG: Error setting initial for {fname}: {e}")
                        else:
                            # Regular model fields - just set initial
                            try:
                                self.fields[fname].initial = val
                                print(f"DEBUG: Set model field initial for '{fname}' = '{val}'")
                            except Exception:
                                pass
        except Exception as e:
            print(f"DEBUG: Error in prefill logic: {e}")
            import traceback
            traceback.print_exc()
        else:
            print(f"DEBUG: ===== PREFILL COMPLETE =====")
            print(f"DEBUG: Final form.initial: {self.initial}")
            print(f"DEBUG: Checking extra__ fields:")
            for fname in [f for f in all_form_fields if f.startswith('extra__')]:
                field = self.fields[fname]
                print(f"DEBUG: {fname} - field.initial: {getattr(field, 'initial', 'NOT SET')}")
                if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                    print(f"DEBUG: {fname} - widget.attrs: {field.widget.attrs}")

    def clean(self):
        cleaned = super().clean()
        if "status" in self.fields and cleaned.get("status") in (None, "",):
            cleaned["status"] = self.initial.get("status", "active")
        if "is_active" in self.fields and cleaned.get("is_active") in (None, ""):
            cleaned["is_active"] = True
        if "active" in self.fields and cleaned.get("active") in (None, ""):
            cleaned["active"] = 1

        if getattr(self.instance, "pk", None):
            explicit = {"voucher_no", "smtcode", "empcode", "staffcode", "VCode"}
            dynamic = {nm for nm in self.fields if nm.lower() == "code" or nm.lower().endswith("code")}
            for nm in (dynamic | explicit):
                if nm in self.fields and cleaned.get(nm) in (None, ""):
                    try:
                        cleaned[nm] = getattr(self.instance, nm)
                    except Exception:
                        pass

        # Global foreign key field handler
        try:
            for field_name, field in self.fields.items():
                if hasattr(field, 'queryset') and field.queryset is not None:
                    # This is a foreign key field
                    if field_name in cleaned and cleaned[field_name]:
                        value = cleaned[field_name]
                        if isinstance(value, str) and value.isdigit():
                            try:
                                # Try to get the related object
                                model_class = field.queryset.model
                                obj = model_class.objects.get(pk=int(value))
                                cleaned[field_name] = obj
                                print(f"DEBUG: Converted {field_name} from '{value}' to {obj}")
                            except model_class.DoesNotExist:
                                print(f"DEBUG: {field_name} with ID {value} does not exist")
                                # Don't add error, just keep the original value
                            except Exception as e:
                                print(f"DEBUG: Error handling {field_name}: {e}")
        except Exception as e:
            print(f"DEBUG: Error in global foreign key handler: {e}")

        return cleaned

    def _convert_foreign_keys_to_dropdowns(self):
        """Automatically convert foreign key fields to proper dropdowns with active record filtering."""
        try:
            if not hasattr(self, 'instance') or not self.instance:
                return
                
            from django.db import models
            model = self.instance._meta.model
            for field_name, field in self.fields.items():
                # Skip extra__ fields as they don't exist in the model
                if field_name.startswith('extra__'):
                    continue
                    
                # Check if this is a foreign key field
                if hasattr(field, 'queryset') and field.queryset is not None:
                    # This is already a ModelChoiceField, ensure it has proper styling
                    if not isinstance(field.widget, forms.Select):
                        field.widget = forms.Select(attrs={"class": "form-control"})
                    continue
                
                # Check if the field exists in the model and is a foreign key
                try:
                    model_field = model._meta.get_field(field_name)
                    if isinstance(model_field, models.ForeignKey):
                        # Convert to ModelChoiceField with active record filtering
                        related_model = model_field.related_model
                        if related_model:
                            # Check if the related model has a status field
                            if hasattr(related_model, '_meta') and any(f.name == 'status' for f in related_model._meta.fields):
                                # Try to order by name, but fall back to other fields if name doesn't exist
                                try:
                                    queryset = related_model.objects.filter(status="active").order_by("name")
                                except:
                                    # Fallback ordering for models without 'name' field
                                    if hasattr(related_model, '_meta') and any(f.name == 'username' for f in related_model._meta.fields):
                                        queryset = related_model.objects.filter(status="active").order_by("username")
                                    elif hasattr(related_model, '_meta') and any(f.name == 'code' for f in related_model._meta.fields):
                                        queryset = related_model.objects.filter(status="active").order_by("code")
                                    else:
                                        queryset = related_model.objects.filter(status="active")
                            else:
                                # Try to order by name, but fall back to other fields if name doesn't exist
                                try:
                                    queryset = related_model.objects.all().order_by("name")
                                except:
                                    # Fallback ordering for models without 'name' field
                                    if hasattr(related_model, '_meta') and any(f.name == 'username' for f in related_model._meta.fields):
                                        queryset = related_model.objects.all().order_by("username")
                                    elif hasattr(related_model, '_meta') and any(f.name == 'code' for f in related_model._meta.fields):
                                        queryset = related_model.objects.all().order_by("code")
                                    else:
                                        queryset = related_model.objects.all()
                            
                            self.fields[field_name] = forms.ModelChoiceField(
                                queryset=queryset,
                                required=field.required,
                                widget=forms.Select(attrs={"class": "form-control"}),
                                label=field.label
                            )
                            print(f"DEBUG: Converted {field_name} to ModelChoiceField with {queryset.count()} records")
                except Exception as e:
                    print(f"DEBUG: Error converting {field_name} to dropdown: {e}")
                    continue
        except Exception as e:
            print(f"DEBUG: Error in _convert_foreign_keys_to_dropdowns: {e}")


# ─────────  CORE DOMAIN FORMS  ─────────
class CompanyForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Company
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep code value posted on edit. Use readonly, never disabled.
        if "code" in self.fields:
            self.fields["code"].widget.attrs.setdefault("readonly", "readonly")
            try:
                self.fields["code"].disabled = False
            except Exception:
                pass
        # Logo optional on update
        if "logo" in self.fields:
            try:
                self.fields["logo"].required = False
            except Exception:
                pass

    # Fix: allow editing a company without tripping unique checks on same record
    def clean_code(self):
        code = (self.cleaned_data.get("code") or "").strip()
        if not code and getattr(self.instance, "pk", None):
            # Preserve existing when browsers omit readonly input
            try:
                return self.instance.code
            except Exception:
                return code
        if not code:
            return code
        qs = Company.objects.filter(code__iexact=code)
        if getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Company code already exists.")
        return code


class BranchForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Branch
        fields = "__all__"


class VillageForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Village
        fields = "__all__"


class CenterForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Center
        fields = "__all__"


class GroupForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Group
        fields = "__all__"


class RoleForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Role
        exclude = ExcludeRawCSVDataForm.Meta.exclude + ["permissions"]



class UsersForm(ExcludeRawCSVDataForm):
    # Limited options to keep modal fast. Field still accepts values outside this slice.
    staff = PermissiveModelChoiceField(
        queryset=Staff._base_manager.none(),  # set in __init__
        required=False,
        error_messages={"invalid_choice": "Selected staff is not available."},
        label="Staff",
    )

    # Override user field to be a text input instead of select
    user = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter a unique username",
            "autocomplete": "off",
        }),
        help_text="Type a username; a Django user will be created or linked.",
        label="User",
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control password-input",
            "placeholder": "Set / Reset password",
            "autocomplete": "new-password",
        }),
        help_text="Leave blank to keep existing password.",
        label="Password",
    )

    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Users
        fields = [
            "staff", "password", "full_name", "branch", "department", "mobile", "status"
        ]
        exclude = ["user"]  # user handled manually
        
        # Explicitly define foreign key fields as dropdowns
        branch = forms.ModelChoiceField(
            queryset=None,  # Will be set in __init__
            required=False,
            widget=forms.Select(attrs={"class": "form-control"}),
            label="Branch"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        print("DEBUG: UsersForm.__init__ called")
        print(f"DEBUG: Form fields: {list(self.fields.keys())}")

        # Set required fields
        if 'full_name' in self.fields:
            self.fields['full_name'].required = True
        if 'staff' in self.fields:
            self.fields['staff'].required = True

        # Set up staff queryset - exclude staff who already have users
        staff_with_users = Users.objects.filter(staff__isnull=False).values_list('staff_id', flat=True)
        base_qs = (Staff._base_manager
                   .filter(status="active")
                   .exclude(staffcode__isnull=True)
                   .exclude(staffcode="")
                   .exclude(id__in=staff_with_users)  # Exclude staff who already have users
                   .only("id", "staffcode", "name")
                   .order_by("name", "staffcode")[:200])
        self.fields["staff"].queryset = base_qs
        print(f"DEBUG: UsersForm.__init__ - staff queryset count: {base_qs.count()}")
        print(f"DEBUG: UsersForm.__init__ - staff queryset values: {list(base_qs.values_list('name', 'staffcode'))}")
        print(f"DEBUG: UsersForm.__init__ - staff with users count: {staff_with_users.count()}")
        
        # Set up branch queryset
        try:
            from .models import Branch
            self.fields["branch"].queryset = Branch.objects.filter(status="active").order_by("name")
            print(f"DEBUG: UsersForm.__init__ - branch queryset count: {self.fields['branch'].queryset.count()}")
        except Exception as e:
            print(f"DEBUG: Error setting branch queryset in UsersForm: {e}")

        # Add user field manually since it's excluded from form fields
        self.fields['user'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter a unique username",
                "autocomplete": "off",
            }),
            help_text="Type a username; a Django user will be created or linked.",
            label="User",
        )

        # Ensure all fields are visible and properly configured
        for field_name, field in self.fields.items():
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                field.widget.attrs.setdefault('class', 'form-control')
        
        # Add validation for mobile field
        if 'mobile' in self.fields:
            self.fields['mobile'].widget.attrs.update({
                'pattern': '[0-9]{10}',
                'title': 'Please enter exactly 10 digits',
                'maxlength': '10',
                'inputmode': 'numeric',
                'placeholder': 'Enter 10 digit number'
            })
                


        # Simple field ordering - only order fields that exist
        try:
            existing_fields = list(self.fields.keys())
            priority_fields = ["staff", "user", "password"]
            
            # Move priority fields to front if they exist
            for field in priority_fields:
                if field in existing_fields:
                    existing_fields.remove(field)
                    existing_fields.insert(0, field)
            
            # Apply the ordering
            self.order_fields(existing_fields)
        except Exception as e:
            print(f"Field ordering error: {e}")
            pass

    def clean_user(self):
        user = self.cleaned_data.get("user")
        if not user:
            return user
        
        # Simple validation - just check if it's a valid string
        if not isinstance(user, str) or not user.strip():
            raise forms.ValidationError("Please enter a valid username.")
        
        return user.strip()
    
    def clean_staff(self):
        staff = self.cleaned_data.get("staff")
        if not staff:
            return staff
        if str(getattr(staff, "status", "")).lower() not in {"active", "1", "true"}:
            raise forms.ValidationError("Selected staff is inactive.")
        
        # Check if this staff already has a user profile
        existing_user = Users.objects.filter(staff=staff)
        if getattr(self.instance, "pk", None):
            existing_user = existing_user.exclude(pk=self.instance.pk)
        
        if existing_user.exists():
            raise forms.ValidationError("This staff member already has a user profile. Only one user per staff is allowed.")
        
        return staff

    def clean_branch(self):
        branch = self.cleaned_data.get("branch")
        if not branch:
            return branch
        
        # If branch is a string (name), try to find the branch by name
        if isinstance(branch, str):
            try:
                from .models import Branch
                branch_obj = Branch.objects.filter(name__iexact=branch, status="active").first()
                if branch_obj:
                    return branch_obj
                else:
                    raise forms.ValidationError("Selected branch is not available or inactive.")
            except Exception:
                raise forms.ValidationError("Invalid branch selection.")
        
        # If branch is already a Branch object, validate it's active
        if hasattr(branch, 'status') and str(branch.status).lower() not in {"active", "1", "true"}:
            raise forms.ValidationError("Selected branch is inactive.")
        
        return branch

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate mobile number format (exactly 10 digits)
        mobile = cleaned_data.get("mobile")
        if mobile:
            print(f"DEBUG: Validating mobile: {mobile}")
            clean_mobile = str(mobile).replace(" ", "")
            print(f"DEBUG: Clean mobile: '{clean_mobile}', length: {len(clean_mobile)}")
            if not clean_mobile.isdigit() or len(clean_mobile) != 10:
                print(f"DEBUG: Mobile validation failed - not 10 digits or not numeric")
                self.add_error("mobile", "Mobile number must be exactly 10 digits")
            else:
                # Update with cleaned mobile number
                cleaned_data["mobile"] = clean_mobile
                print(f"DEBUG: Mobile validation passed, cleaned: {clean_mobile}")
        
        # Ensure user gets staff status - all users get staff status
        if cleaned_data.get("user"):
            pass
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle user field conversion from string to Django User instance
        user_username = self.cleaned_data.get('user')
        if user_username:
            from django.contrib.auth.models import User as AuthUser
            # Try to get existing user or create new one
            auth_user, created = AuthUser.objects.get_or_create(
                username=user_username,
                defaults={
                    'first_name': self.cleaned_data.get('full_name', '').split()[0] if self.cleaned_data.get('full_name') else '',
                    'last_name': ' '.join(self.cleaned_data.get('full_name', '').split()[1:]) if self.cleaned_data.get('full_name') and len(self.cleaned_data.get('full_name', '').split()) > 1 else '',
                    'email': f"{user_username}@example.com",  # Default email
                    'is_active': True,
                }
            )
            instance.user = auth_user
            
            # Set password if provided
            password = self.cleaned_data.get('password')
            if password:
                auth_user.set_password(password)
                auth_user.save()
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance


class UserPermissionForm(ExcludeRawCSVDataForm):
    user_profile = PermissiveModelChoiceField(
        queryset=Users._base_manager.all(),
        required=True,
        error_messages={"invalid_choice": "Selected user is not available."},
        label="User Profile",
    )
    
    # Boolean fields as choice fields with proper Yes/No options
    is_admin = forms.ChoiceField(
        choices=[("True", "Yes"), ("False", "No")],
        required=False,
        label="Is Admin",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    is_master = forms.ChoiceField(
        choices=[("True", "Yes"), ("False", "No")],
        required=False,
        label="Is Master",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    is_data_entry = forms.ChoiceField(
        choices=[("True", "Yes"), ("False", "No")],
        required=False,
        label="Is Data Entry",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    is_accounting = forms.ChoiceField(
        choices=[("True", "Yes"), ("False", "No")],
        required=False,
        label="Is Accounting",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    is_recovery_agent = forms.ChoiceField(
        choices=[("True", "Yes"), ("False", "No")],
        required=False,
        label="Is Recovery Agent",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    is_auditor = forms.ChoiceField(
        choices=[("True", "Yes"), ("False", "No")],
        required=False,
        label="Is Auditor",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    is_manager = forms.ChoiceField(
        choices=[("True", "Yes"), ("False", "No")],
        required=False,
        label="Is Manager",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta(ExcludeRawCSVDataForm.Meta):
        model = UserPermission
        fields = ["user_profile", "is_admin", "is_master", "is_data_entry", 
                 "is_accounting", "is_recovery_agent", "is_auditor", "is_manager", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values for boolean fields based on instance
        if self.instance and self.instance.pk:
            boolean_fields = ['is_admin', 'is_master', 'is_data_entry', 
                             'is_accounting', 'is_recovery_agent', 'is_auditor', 'is_manager']
            for field_name in boolean_fields:
                if field_name in self.fields:
                    value = getattr(self.instance, field_name, False)
                    self.fields[field_name].initial = "True" if value else "False"
        
        want_first = ["user_profile", "is_admin", "is_master", "is_data_entry",
                      "is_accounting", "is_recovery_agent", "is_auditor", "is_manager", "status"]
        ordered = [f for f in want_first if f in self.fields] + \
                  [f for f in self.fields if f not in want_first]
        try:
            self.order_fields(ordered)
        except Exception:
            pass

        try:
            field = self.fields.get("user_profile")
            if field:
                # Exclude user profiles that already have a UserPermission
                from django.db.models import Q
                qs = Users._base_manager.select_related("staff", "branch").all()

                current_id = None
                try:
                    if self.instance and getattr(self.instance, "pk", None):
                        current_id = getattr(getattr(self.instance, "user_profile", None), "pk", None)
                except Exception:
                    current_id = None

                if current_id:
                    qs = qs.filter(Q(permissions_set__isnull=True) | Q(pk=current_id))
                else:
                    qs = qs.filter(permissions_set__isnull=True)

                def _label(up):
                    name = ""
                    try:
                        name = (getattr(getattr(up, "staff", None), "name", "") or
                                getattr(up, "full_name", "") or "")
                    except Exception:
                        pass
                    if not name:
                        try:
                            name = getattr(up, "full_name", "") or ""
                        except Exception:
                            pass
                    if not name:
                        try:
                            user_field = Users._meta.get_field("user")
                            if isinstance(user_field, ForeignKey):
                                name = getattr(getattr(up, "user", None), "username", "") or ""
                            else:
                                name = getattr(up, "user", "") or ""
                        except Exception:
                            name = getattr(up, "user", "") or ""
                    if not name:
                        name = f"UserProfile #{up.pk}"
                    try:
                        bname = getattr(getattr(up, "branch", None), "name", "") or ""
                        if bname:
                            name = f"{name} — {bname}"
                    except Exception:
                        pass
                    return name

                field.queryset = qs
                field.empty_label = "— select —"
                field.widget.choices = [("", "— select —")] + [(str(up.pk), _label(up)) for up in qs]
        except Exception:
            pass

    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure boolean fields are properly converted
        boolean_fields = ['is_admin', 'is_master', 'is_data_entry', 
                         'is_accounting', 'is_recovery_agent', 'is_auditor', 'is_manager']
        
        for field_name in boolean_fields:
            if field_name in cleaned_data:
                value = cleaned_data[field_name]
                # Convert string "True"/"False" to actual boolean
                if isinstance(value, str):
                    cleaned_data[field_name] = value.lower() in ('true', '1', 'yes', 'on')
                elif isinstance(value, bool):
                    cleaned_data[field_name] = value
                else:
                    cleaned_data[field_name] = bool(value)
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Ensure boolean fields are properly set
        boolean_fields = ['is_admin', 'is_master', 'is_data_entry', 
                         'is_accounting', 'is_recovery_agent', 'is_auditor', 'is_manager']
        
        for field_name in boolean_fields:
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                # Convert to proper boolean
                if isinstance(value, str):
                    setattr(instance, field_name, value.lower() in ('true', '1', 'yes', 'on'))
                else:
                    setattr(instance, field_name, bool(value))
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance


class StaffForm(ExcludeRawCSVDataForm):
    contact1 = forms.CharField(
        validators=[phone_validator], 
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "pattern": "[0-9]{10}",
            "title": "Please enter exactly 10 digits",
            "maxlength": "10",
            "inputmode": "numeric",
            "placeholder": "Enter 10 digit number"
        })
    )
    
    # Custom Aadhaar field with proper widget
    extra__aadhaar_number = forms.CharField(
        required=False,
        max_length=14,  # 12 digits + 2 spaces
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "pattern": "[0-9]{4} [0-9]{4} [0-9]{4}",
            "title": "Please enter Aadhaar in format: 0000 0000 0000",
            "maxlength": "14",
            "inputmode": "numeric",
            "placeholder": "0000 0000 0000"
        })
    )
    
    # Custom Aadhaar validator
    def clean_extra__aadhaar_number(self):
        print(f"DEBUG: Validating Aadhaar number: {self.cleaned_data.get('extra__aadhaar_number')}")
        aadhaar = self.cleaned_data.get("extra__aadhaar_number")
        if aadhaar:
            # Remove spaces and check if it's exactly 12 digits
            clean_aadhaar = str(aadhaar).replace(" ", "")
            print(f"DEBUG: Clean Aadhaar: '{clean_aadhaar}', length: {len(clean_aadhaar)}")
            if not clean_aadhaar.isdigit() or len(clean_aadhaar) != 12:
                print(f"DEBUG: Aadhaar validation failed - not 12 digits or not numeric")
                raise forms.ValidationError("Aadhaar number must be exactly 12 digits")
            
            # Format as 0000 0000 0000
            formatted_aadhaar = f"{clean_aadhaar[:4]} {clean_aadhaar[4:8]} {clean_aadhaar[8:12]}"
            print(f"DEBUG: Aadhaar formatted: '{formatted_aadhaar}'")
            return formatted_aadhaar
        return aadhaar
    
    # Custom emergency contact field with proper widget
    extra__emergency_contact = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "pattern": "[0-9]{10}",
            "title": "Please enter exactly 10 digits",
            "maxlength": "10",
            "inputmode": "numeric",
            "placeholder": "Enter 10 digit number"
        })
    )
    
    # Custom date of birth field with proper widget
    extra__date_of_birth = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "date-field form-control",
            "placeholder": "dd/mm/yyyy",
            "data-flatpickr": "true",
            "autocomplete": "off",
            "pattern": "\\d{2}/\\d{2}/\\d{4}",
            "maxlength": "10",
            "title": "Please enter date in dd/mm/yyyy format"
        })
    )
    
    # Custom emergency contact validator
    def clean_extra__emergency_contact(self):
        print(f"DEBUG: Validating emergency contact: {self.cleaned_data.get('extra__emergency_contact')}")
        emergency_contact = self.cleaned_data.get("extra__emergency_contact")
        if emergency_contact:
            # Remove spaces and check if it's exactly 10 digits
            clean_contact = str(emergency_contact).replace(" ", "")
            print(f"DEBUG: Clean emergency contact: '{clean_contact}', length: {len(clean_contact)}")
            if not clean_contact.isdigit() or len(clean_contact) != 10:
                print(f"DEBUG: Emergency contact validation failed - not 10 digits or not numeric")
                raise forms.ValidationError("Emergency contact must be exactly 10 digits")
            return clean_contact
        return emergency_contact
    
    # Explicitly define foreign key fields as dropdowns
    branch = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Branch"
    )
    
    cadre = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Cadre"
    )

    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Staff
        fields = [
            "staffcode", "name", "branch", "cadre", "designation", "joining_date", 
            "status", "bank", "ifsc", "contact1", "photo"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ensure our custom field definitions take precedence
        try:
            from .models import Branch, Cadre
            
            # Force branch field to be ModelChoiceField
            if "branch" in self.fields:
                self.fields["branch"] = forms.ModelChoiceField(
                    queryset=Branch.objects.filter(status="active").order_by("name"),
                    required=False,
                    widget=forms.Select(attrs={"class": "form-control"}),
                    label="Branch"
                )
                print(f"DEBUG: Forced branch field to ModelChoiceField with {self.fields['branch'].queryset.count()} active branches")
        except Exception as e:
            print(f"DEBUG: Error setting branch field: {e}")
        
        try:
            # Force cadre field to be ModelChoiceField
            if "cadre" in self.fields:
                self.fields["cadre"] = forms.ModelChoiceField(
                    queryset=Cadre.objects.filter(status="active"),
                    required=False,
                    widget=forms.Select(attrs={"class": "form-control"}),
                    label="Cadre"
                )
                print(f"DEBUG: Forced cadre field to ModelChoiceField with {self.fields['cadre'].queryset.count()} active cadres")
        except Exception as e:
            print(f"DEBUG: Error setting cadre field: {e}")
        
        # Make joining_date field unchangeable (read-only)
        if "joining_date" in self.fields:
            # Always make joining_date read-only, whether creating or editing
            self.fields["joining_date"].widget.attrs.update({
                "readonly": "readonly",
                "disabled": "disabled",
                "class": "form-control bg-light",
                "title": "Joining date cannot be changed",
                "style": "background-color: #f8f9fa; cursor: not-allowed;"
            })
            
            # If this is an edit (instance exists), make it completely unchangeable
            if hasattr(self, 'instance') and self.instance and self.instance.pk:
                # For existing records, make the field completely unchangeable
                self.fields["joining_date"].widget.attrs.update({
                    "data-original-value": str(self.instance.joining_date) if self.instance.joining_date else "",
                    "data-edit-mode": "true",
                    "data-protected": "true",
                    "aria-label": "Joining date (cannot be changed)",
                    "tabindex": "-1"  # Remove from tab order
                })
                print(f"DEBUG: Made joining_date field completely unchangeable for edit (ID: {self.instance.pk})")
            else:
                print(f"DEBUG: Made joining_date field read-only for new record")
        
        if "photo" in self.fields:
            self.fields["photo"].widget = ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
                "capture": "environment"
            })

    def clean(self):
        cleaned_data = super().clean()
        print(f"DEBUG: StaffForm.clean() called with data: {cleaned_data}")
        
        # For existing records, prevent joining_date from being changed
        if self.instance and self.instance.pk and self.instance.joining_date:
            original_joining_date = self.instance.joining_date
            new_joining_date = cleaned_data.get('joining_date')
            
            # If someone tries to change the joining_date, restore the original
            if new_joining_date and new_joining_date != original_joining_date:
                print(f"DEBUG: Attempted to change joining_date from {original_joining_date} to {new_joining_date} - preventing change")
                cleaned_data['joining_date'] = original_joining_date
                # Don't add error, just silently restore the original value
                # This ensures the field appears unchanged in the form
        
        contact = cleaned_data.get("contact1")
        print(f"DEBUG: Validating contact1: {contact}")

        # Validate contact1 format (exactly 10 digits)
        if contact:
            clean_contact = str(contact).replace(" ", "")
            print(f"DEBUG: Clean contact: '{clean_contact}', length: {len(clean_contact)}")
            if not clean_contact.isdigit() or len(clean_contact) != 10:
                print(f"DEBUG: Contact validation failed - not 10 digits or not numeric")
                self.add_error("contact1", "Contact number must be exactly 10 digits")
            else:
                # Check for duplicate contact numbers
                if Staff._base_manager.exclude(pk=self.instance.pk)\
                        .filter(contact1=clean_contact).exists():
                    self.add_error("contact1", "Contact number already exists.")
                else:
                    # Update with cleaned contact number
                    cleaned_data["contact1"] = clean_contact
                    print(f"DEBUG: Contact validation passed, cleaned: {clean_contact}")

        # Validate Aadhaar number if present
        aadhaar = cleaned_data.get("extra__aadhaar_number")
        if aadhaar:
            print(f"DEBUG: Validating Aadhaar in clean method: {aadhaar}")
            clean_aadhaar = str(aadhaar).replace(" ", "")
            if not clean_aadhaar.isdigit() or len(clean_aadhaar) != 12:
                print(f"DEBUG: Aadhaar validation failed in clean method")
                self.add_error("extra__aadhaar_number", "Aadhaar number must be exactly 12 digits")
            else:
                # Format as 0000 0000 0000
                formatted_aadhaar = f"{clean_aadhaar[:4]} {clean_aadhaar[4:8]} {clean_aadhaar[8:12]}"
                cleaned_data["extra__aadhaar_number"] = formatted_aadhaar
                print(f"DEBUG: Aadhaar validation passed, formatted: {formatted_aadhaar}")

        # Validate emergency contact if present
        emergency_contact = cleaned_data.get("extra__emergency_contact")
        if emergency_contact:
            print(f"DEBUG: Validating emergency contact in clean method: {emergency_contact}")
            clean_emergency = str(emergency_contact).replace(" ", "")
            if not clean_emergency.isdigit() or len(clean_emergency) != 10:
                print(f"DEBUG: Emergency contact validation failed in clean method")
                self.add_error("extra__emergency_contact", "Emergency contact must be exactly 10 digits")
            else:
                cleaned_data["extra__emergency_contact"] = clean_emergency
                print(f"DEBUG: Emergency contact validation passed, cleaned: {clean_emergency}")

        # Validate date of birth if present
        date_of_birth = cleaned_data.get("extra__date_of_birth")
        if date_of_birth:
            print(f"DEBUG: Validating date of birth in clean method: {date_of_birth}")
            # Convert dd/mm/yyyy to YYYY-MM-DD for storage
            try:
                if isinstance(date_of_birth, str) and '/' in date_of_birth:
                    day, month, year = date_of_birth.split('/')
                    from datetime import date
                    dob_date = date(int(year), int(month), int(day))
                    cleaned_data["extra__date_of_birth"] = dob_date.isoformat()
                    print(f"DEBUG: Date of birth converted to: {dob_date.isoformat()}")
                elif hasattr(date_of_birth, 'isoformat'):
                    cleaned_data["extra__date_of_birth"] = date_of_birth.isoformat()
                    print(f"DEBUG: Date of birth already in ISO format: {date_of_birth.isoformat()}")
            except Exception as e:
                print(f"DEBUG: Error converting date of birth: {e}")
                self.add_error("extra__date_of_birth", "Please enter a valid date in dd/mm/yyyy format")

        # Handle foreign key fields that might come as strings
        try:
            if "branch" in cleaned_data and cleaned_data["branch"]:
                branch_id = cleaned_data["branch"]
                if isinstance(branch_id, str) and branch_id.isdigit():
                    from .models import Branch
                    try:
                        branch = Branch.objects.get(pk=int(branch_id))
                        cleaned_data["branch"] = branch
                    except Branch.DoesNotExist:
                        self.add_error("branch", "Selected branch does not exist.")
                elif not isinstance(branch_id, Branch):
                    self.add_error("branch", "Invalid branch selection.")
        except Exception as e:
            print(f"DEBUG: Error handling branch field: {e}")
        
        # Validate joining date if present
        joining_date = cleaned_data.get("joining_date")
        if joining_date:
            print(f"DEBUG: Validating joining date: {joining_date}")
            try:
                if isinstance(joining_date, str) and '/' in joining_date:
                    day, month, year = joining_date.split('/')
                    from datetime import date
                    join_date = date(int(year), int(month), int(day))
                    cleaned_data["joining_date"] = join_date
                    print(f"DEBUG: Joining date converted to: {join_date}")
                elif hasattr(joining_date, 'isoformat'):
                    print(f"DEBUG: Joining date already a date object: {joining_date}")
            except Exception as e:
                print(f"DEBUG: Error converting joining date: {e}")
                self.add_error("joining_date", "Please enter a valid date in dd/mm/yyyy format")

        try:
            if "cadre" in cleaned_data and cleaned_data["cadre"]:
                cadre_id = cleaned_data["cadre"]
                if isinstance(cadre_id, str) and cadre_id.isdigit():
                    from .models import Cadre
                    try:
                        cadre = Cadre.objects.get(pk=int(cadre_id))
                        cleaned_data["cadre"] = cadre
                    except Cadre.DoesNotExist:
                        self.add_error("cadre", "Selected cadre does not exist.")
                    except Exception:
                        # Cadre model might not exist, skip this validation
                        pass
                elif not hasattr(cadre_id, 'pk'):
                    self.add_error("cadre", "Invalid cadre selection.")
        except Exception as e:
            print(f"DEBUG: Error handling cadre field: {e}")

        # Handle date fields that might come in different formats
        try:
            if "joining_date" in cleaned_data and cleaned_data["joining_date"]:
                joining_date = cleaned_data["joining_date"]
                if isinstance(joining_date, str):
                    # Convert dd/mm/yyyy to yyyy-mm-dd if needed
                    if len(joining_date) == 10 and joining_date[2] == '/' and joining_date[5] == '/':
                        try:
                            d, m, y = joining_date.split('/')
                            from datetime import datetime
                            parsed_date = datetime(int(y), int(m), int(d)).date()
                            cleaned_data["joining_date"] = parsed_date
                            print(f"DEBUG: Converted joining_date from '{joining_date}' to {parsed_date}")
                        except Exception as e:
                            print(f"DEBUG: Error parsing joining_date '{joining_date}': {e}")
        except Exception as e:
            print(f"DEBUG: Error handling joining_date: {e}")

        # Handle extra__date_of_birth field
        try:
            if "extra__date_of_birth" in cleaned_data and cleaned_data["extra__date_of_birth"]:
                dob = cleaned_data["extra__date_of_birth"]
                if isinstance(dob, str):
                    # Convert dd/mm/yyyy to yyyy-mm-dd if needed
                    if len(dob) == 10 and dob[2] == '/' and dob[5] == '/':
                        try:
                            d, m, y = dob.split('/')
                            from datetime import datetime
                            parsed_dob = datetime(int(y), int(m), int(d)).date()
                            cleaned_data["extra__date_of_birth"] = parsed_dob
                            print(f"DEBUG: Converted extra__date_of_birth from '{dob}' to {parsed_dob}")
                        except Exception as e:
                            print(f"DEBUG: Error parsing extra__date_of_birth '{dob}': {e}")
        except Exception as e:
            print(f"DEBUG: Error handling extra__date_of_birth: {e}")

        return cleaned_data
    
    def clean_joining_date(self):
        """Custom validation for joining_date field - prevents changes on edit"""
        joining_date = self.cleaned_data.get('joining_date')
        
        # For existing records, prevent any changes to joining_date
        if self.instance and self.instance.pk and self.instance.joining_date:
            original_joining_date = self.instance.joining_date
            if joining_date and joining_date != original_joining_date:
                print(f"DEBUG: clean_joining_date: Attempted to change from {original_joining_date} to {joining_date} - preventing change")
                # Return the original value instead of the new one
                return original_joining_date
        
        return joining_date

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            self.save_m2m()
        return instance


class ProductForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Product
        fields = "__all__"



    def clean(self):
        cleaned_data = super().clean()
        aadhar = cleaned_data.get("aadhar")
        contact = cleaned_data.get("contactno")

        # Validate Aadhaar number format (exactly 12 digits)
        if aadhar:
            clean_aadhar = str(aadhar).replace(" ", "")
            if not clean_aadhar.isdigit() or len(clean_aadhar) != 12:
                self.add_error("aadhar", "Aadhaar number must be exactly 12 digits")
            else:
                # Format as 0000 0000 0000
                formatted_aadhar = f"{clean_aadhar[:4]} {clean_aadhar[4:8]} {clean_aadhar[8:12]}"
                cleaned_data["aadhar"] = formatted_aadhar
                
                # Check for duplicate Aadhaar
                if Client._base_manager.exclude(pk=self.instance.pk)\
                        .filter(aadhar=formatted_aadhar).exists():
                    self.add_error("aadhar", "Aadhaar number already exists.")

        # Validate contact number format (exactly 10 digits)
        if contact:
            clean_contact = str(contact).replace(" ", "")
            if not clean_contact.isdigit() or len(clean_contact) != 10:
                self.add_error("contactno", "Contact number must be exactly 10 digits")
            else:
                # Update with cleaned contact number
                cleaned_data["contactno"] = clean_contact
                
                # Check for duplicate contact
                if Client._base_manager.exclude(pk=self.instance.pk)\
                        .filter(contactno=clean_contact).exists():
                    self.add_error("contactno", "Contact number already exists.")

        return cleaned_data


class LoanApplicationForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanApplication
        fields = "__all__"


class LoanApprovalForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanApproval
        fields = "__all__"


class DisbursementForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Disbursement
        fields = "__all__"


class PrepaidForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Prepaid
        fields = "__all__"


class MortgageForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Mortgage
        fields = "__all__"


class ExSavingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = ExSaving
        fields = "__all__"


class FieldScheduleForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = FieldSchedule
        fields = "__all__"


class FieldReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = FieldReport
        fields = "__all__"


class WeeklyReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = WeeklyReport
        fields = "__all__"


class MonthlyReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = MonthlyReport
        fields = "__all__"


class BusinessSettingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = BusinessSetting
        fields = "__all__"


class AccountHeadForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = AccountHead
        fields = "__all__"


class VoucherForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Voucher
        fields = "__all__"


class PostingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Posting
        fields = "__all__"


class RecoveryPostingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = RecoveryPosting
        fields = "__all__"


class AppointmentForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Appointment
        fields = "__all__"


class SalaryStatementForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = SalaryStatement
        fields = "__all__"


class PaymentForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Payment
        fields = "__all__"


class RepaymentForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Repayment
        fields = "__all__"


class LoanRestructureForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanRestructure
        fields = "__all__"


class NotificationForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Notification
        fields = "__all__"


class GatewayEventForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = GatewayEvent
        fields = "__all__"


class EWIFlagForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = EWIFlag
        fields = "__all__"


class KYCDocumentForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = KYCDocument
        fields = "__all__"


class AlertRuleForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = AlertRule
        fields = "__all__"


class ColumnForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Column
        fields = "__all__"


class CadreForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Cadre
        fields = "__all__"


class ClientForm(ExcludeRawCSVDataForm):
    # Explicitly define foreign key fields as dropdowns
    group = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Group"
    )
    
    aadhar = forms.CharField(
        required=False,
        max_length=14,  # 12 digits + 2 spaces
        widget=TextInput(attrs={
            "class": "form-control",
            "pattern": "[0-9]{4} [0-9]{4} [0-9]{4}",
            "title": "Please enter Aadhaar in format: 0000 0000 0000",
            "maxlength": "14",
            "inputmode": "numeric",
            "placeholder": "0000 0000 0000"
        })
    )
    contactno = forms.CharField(
        required=False,
        max_length=10,
        widget=TextInput(attrs={
            "class": "form-control",
            "pattern": "[0-9]{10}",
            "title": "Please enter exactly 10 digits",
            "maxlength": "10",
            "inputmode": "numeric",
            "placeholder": "Enter 10 digit number"
        })
    )

    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Client
        fields = [
            "smtcode", "name", "group", "gender", "aadhar", "contactno", 
            "join_date", "status"
        ]

    def clean(self):
        cleaned_data = super().clean()
        print(f"DEBUG: ClientForm.clean() called with data: {cleaned_data}")
        
        aadhar = cleaned_data.get("aadhar")
        contact = cleaned_data.get("contactno")

        # Validate Aadhaar number format
        if aadhar:
            print(f"DEBUG: Validating Aadhaar: {aadhar}")
            clean_aadhaar = str(aadhaar).replace(" ", "")
            if not clean_aadhaar.isdigit() or len(clean_aadhaar) != 12:
                print(f"DEBUG: Aadhaar validation failed - not 12 digits or not numeric")
                self.add_error("aadhar", "Aadhaar number must be exactly 12 digits")
            else:
                # Format as 0000 0000 0000
                formatted_aadhaar = f"{clean_aadhaar[:4]} {clean_aadhaar[4:8]} {clean_aadhaar[8:12]}"
                cleaned_data["aadhar"] = formatted_aadhaar
                print(f"DEBUG: Aadhaar validation passed, formatted: {formatted_aadhaar}")
                
                # Check for duplicates
                if Client.objects.exclude(pk=self.instance.pk).filter(aadhaar=formatted_aadhaar).exists():
                    self.add_error("aadhar", "Aadhaar number already exists.")

        # Validate contact number format
        if contact:
            print(f"DEBUG: Validating contact: {contact}")
            clean_contact = str(contact).replace(" ", "")
            if not clean_contact.isdigit() or len(clean_contact) != 10:
                print(f"DEBUG: Contact validation failed - not 10 digits or not numeric")
                self.add_error("contactno", "Contact number must be exactly 10 digits")
            else:
                cleaned_data["contactno"] = clean_contact
                print(f"DEBUG: Contact validation passed, cleaned: {clean_contact}")
                
                # Check for duplicates
                if Client.objects.exclude(pk=self.instance.pk).filter(contactno=clean_contact).exists():
                    self.add_error("contactno", "Contact number already exists.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set querysets for foreign key fields to show only active records
        try:
            from .models import Group
            
            # Set group field queryset to show only active groups
            if "group" in self.fields:
                self.fields["group"] = forms.ModelChoiceField(
                    queryset=Group.objects.filter(status="active").order_by("name"),
                    required=False,
                    widget=forms.Select(attrs={"class": "form-control"}),
                    label="Group"
                )
                print(f"DEBUG: Set group field to ModelChoiceField with {self.fields['group'].queryset.count()} active groups")
        except Exception as e:
            print(f"DEBUG: Error setting group field: {e}")


class LoanApplicationForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanApplication
        fields = "__all__"


class LoanApprovalForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanApproval
        fields = "__all__"


class DisbursementForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Disbursement
        fields = "__all__"


class BusinessSettingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = BusinessSetting
        fields = "__all__"


class FieldScheduleForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = FieldSchedule
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from django.db.models import Q
            if "staff" in self.fields:
                self.fields["staff"].queryset = Staff._base_manager.filter(
                    Q(status="active") | Q(status=1) | Q(status="1") | Q(status=True)
                ).order_by("name")
        except Exception:
            pass


class FieldReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = FieldReport
        fields = "__all__"


class WeeklyReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = WeeklyReport
        fields = "__all__"


class MonthlyReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = MonthlyReport
        fields = "__all__"


class ColumnForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Column
        fields = "__all__"


class CadreForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Cadre
        fields = "__all__"


# ───────── SAVINGS / PREPAID / MORTGAGE (added) ─────────
class PrepaidForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Prepaid
        fields = "__all__"


class MortgageForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Mortgage
        fields = "__all__"


class ExSavingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = ExSaving
        fields = "__all__"


# ───────── FEATURE FORMS (added) ─────────
class KYCDocumentForm(ExcludeRawCSVDataForm):
    """KYC uploads and metadata."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = KYCDocument
        fields = "__all__"


class AlertRuleForm(ExcludeRawCSVDataForm):
    """Alert rules configuration."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = AlertRule
        fields = "__all__"


class AppointmentForm(ExcludeRawCSVDataForm):
    """HRPM appointment entries."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Appointment
        fields = "__all__"


class SalaryStatementForm(ExcludeRawCSVDataForm):
    """HRPM salary statements."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = SalaryStatement
        fields = "__all__"


# ───────── SYNC ADD-ONS: PAYMENTS / RISK / RESTRUCTURE / REPAY ─────────
class PaymentForm(ExcludeRawCSVDataForm):
    """Payment intent creation; order_id is system-generated in views."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Payment
        fields = "__all__"


class NotificationForm(ExcludeRawCSVDataForm):
    """Outbound notifications queue."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Notification
        fields = "__all__"


class GatewayEventForm(ExcludeRawCSVDataForm):
    """Read-only webhook event viewer."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = GatewayEvent
        fields = "__all__"


class EWIFlagForm(ExcludeRawCSVDataForm):
    """Early warning indicator flags."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = EWIFlag
        fields = "__all__"


class LoanRestructureForm(ExcludeRawCSVDataForm):
    """Restructure terms."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanRestructure
        fields = "__all__"


class RepaymentForm(ExcludeRawCSVDataForm):
    """Manual repayment entries (cash or reconciled)."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Repayment
        fields = "__all__"


# ─────────  NEW BUSINESS TABLE FORMS  ─────────
class AccountHeadForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = AccountHead
        fields = "__all__"


class VoucherForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Voucher
        fields = "__all__"


class PostingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Posting
        fields = "__all__"


class RecoveryPostingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = RecoveryPosting
        fields = "__all__"


# ─────────  CUSTOM USERS FORM  ─────────
class UsersForm(ExcludeRawCSVDataForm):
    """Custom form for Users model with proper querysets."""
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Users
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Fix staff queryset - show all active staff
        if 'staff' in self.fields:
            from django.db.models import Q
            print(f"DEBUG: UsersForm.__init__ - staff queryset count: {self.fields['staff'].queryset.count()}")
            print(f"DEBUG: UsersForm.__init__ - staff queryset values: {list(self.fields['staff'].queryset.values_list('id', 'name', 'status'))}")
            
            # Get all staff and check their status
            all_staff = Staff.objects.all()
            print(f"DEBUG: UsersForm.__init__ - staff with users count: {all_staff.count()}")
            
            # Try different status values
            active_staff = Staff.objects.filter(
                Q(status="active") | Q(status=1) | Q(status="1") | Q(status=True)
            )
            print(f"DEBUG: UsersForm.__init__ - available staff count: {active_staff.count()}")
            
            self.fields['staff'].queryset = active_staff.order_by("name")
            print(f"DEBUG: UsersForm.__init__ - final staff queryset count: {self.fields['staff'].queryset.count()}")
            print(f"DEBUG: UsersForm.__init__ - final staff queryset values: {list(self.fields['staff'].queryset.values_list('id', 'name', 'status'))}")
        
        # Fix user queryset - show all active Django users
        if 'user' in self.fields:
            from django.contrib.auth.models import User
            self.fields['user'].queryset = User.objects.filter(
                is_active=True
            ).order_by("username")
        
        # Fix branch queryset - show all active branches
        if 'branch' in self.fields:
            from django.db.models import Q
            self.fields['branch'].queryset = Branch.objects.filter(
                Q(status="active") | Q(status=1) | Q(status="1") | Q(status=True)
            ).order_by("name")

# ─────────  AUTO-GENERATED FORMS FOR CSV TABLES  ─────────
_csv_models = [
    AccCashbook, AccCashbookold, AccHeads, Aadhar, Accfundloancols, Accfundloans,
    Accountmaster, Arrear, Cheque, Codes, Contacts, Dayend, Equity2,
    Equityshare31032014, Equityshare31032015, Gr, Groups, MXAgent, MXCode,
    MXMember, MXSavings, Massposting, MasterBranch, MasterCategories, MasterFs,
    MasterLoanpurposes, MasterLoantypes, MasterMonth, MasterSectors, MasterSetup,
    MasterWeeks, MXAgriment, MXLoancols, MXLoans, MXSalaries, Pdc, RptDaybook,
    Securitydeposit, Staffloans, Transefer, Cobarower, Collectionrpt, Fund,
    Loancols, Loans, Loansmfi41110, Mloanschedule, Mloancols, Mloans, Mlogin,
    Mmisc, Mrecvisit, Msetup, Msurity, MasterBusinessmode, Memberdeposits,
    Members, Memberskaikaluru, Pbdet, Rptincome, RptGrcollectionsheet,
    RptOutstanding, RptPassbook, RptPassbookcommon, RptTb, RptDisRegister,
    RptHigh, RptSavings, RptSumsheet, Savings, Setup, Setupn, Share, Share1,
    Smtavail, Temp  # Note: Users is excluded because we have a custom form
]

for model_cls in _csv_models:
    form_name = f"{model_cls.__name__}Form"
    meta_cls = type("Meta", (ExcludeRawCSVDataForm.Meta,), {
        "model": model_cls,
        "fields": "__all__"
    })
    globals()[form_name] = type(form_name, (ExcludeRawCSVDataForm,), {
        "Meta": meta_cls
    })
