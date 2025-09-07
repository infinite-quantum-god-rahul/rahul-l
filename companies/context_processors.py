# companies/context_processors.py
from companies.views import role_flags, get_profile_for_user

def user_header_info(request):
    # Check if user attribute exists and is authenticated
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {}

    # Display name: prefer full name, fallback to username
    name = request.user.get_full_name() or request.user.username

    # Try to get branch from userprofile first, then fallback to staff_info
    branch_name = ""
    profile = get_profile_for_user(request.user)
    if profile and getattr(profile, "branch", None):
        branch = profile.branch
        branch_name = getattr(branch, "name", str(branch))
    else:
        staff_info = getattr(request.user, "staff_info", None)
        if staff_info and getattr(staff_info, "branch", None):
            branch = staff_info.branch
            branch_name = getattr(branch, "name", str(branch))

    # Get role flags for proper permission system
    role_flags_dict = role_flags(request.user)
    
    # Role label for clarity
    role_label = None
    if request.user.is_superuser:
        role_label = "Superuser"
    elif role_flags_dict.get("admin"):
        role_label = "Admin"
    elif role_flags_dict.get("manager"):
        role_label = "Manager"

    elif role_flags_dict.get("data_entry"):
        role_label = "Data Entry"
    elif role_flags_dict.get("accounting"):
        role_label = "Accounting"
    elif role_flags_dict.get("recovery_agent"):
        role_label = "Recovery Agent"
    elif role_flags_dict.get("auditor"):
        role_label = "Auditor"
    elif request.user.is_staff:
        role_label = "Staff"
    else:
        role_label = "User"

    return {
        "header_user_display_name": name,
        "header_branch_name": branch_name,
        "header_role_label": role_label,
        "role_flags": role_flags_dict,
    }
# companies/context_processors.py
from django.conf import settings

def sml_features(request):
    """
    Make feature flags available in all templates as `SML_FEATURES`.
    Safe if the setting is missing (returns empty dict).
    """
    return {"SML_FEATURES": getattr(settings, "SML_FEATURES", {})}
