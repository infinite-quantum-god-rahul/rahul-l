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
    Company, Branch, Village, Center, Group, Role, Staff, UserCreation,
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
    Smtavail, Temp,
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


def fix_required_attributes(form_obj):
    """
    Fix required attributes for all form fields to prevent "True is not defined" errors.
    This function ensures that Python boolean True values are converted to string "required".
    """
    if not form_obj or not hasattr(form_obj, 'fields'):
        return
    
    try:
        # Create a safe copy of fields to iterate over
        field_items = list(form_obj.fields.items())
        
        for field_name, field in field_items:
            if getattr(field, 'required', False):
                # Ensure required attribute is a string, not boolean
                if 'widget' in field.__dict__ and hasattr(field.widget, 'attrs'):
                    field.widget.attrs['required'] = 'required'
                    field.widget.attrs['data-required'] = 'true'
                else:
                    # If widget doesn't have attrs, create them
                    if not hasattr(field, 'widget'):
                        continue
                    if not hasattr(field.widget, 'attrs'):
                        field.widget.attrs = {}
                    field.widget.attrs['required'] = 'required'
                    field.widget.attrs['data-required'] = 'true'
                    
    except Exception as e:
        # Log the error but don't crash the form
        print(f"Warning: Error fixing required attributes for {form_obj.__class__.__name__}: {e}")
        pass


class SafeRequiredFormRenderer:
    """
    Custom form renderer that ensures required attributes are always rendered correctly.
    This prevents the "True is not defined" JavaScript error.
    """
    
    @staticmethod
    def render_field(field):
        """
        Render a form field with safe required attributes.
        """
        try:
            if hasattr(field, 'field') and getattr(field.field, 'required', False):
                # Ensure the widget has the correct required attributes
                if hasattr(field.field.widget, 'attrs'):
                    field.field.widget.attrs['required'] = 'required'
                    field.field.widget.attrs['data-required'] = 'true'
                else:
                    field.field.widget.attrs = {'required': 'required', 'data-required': 'true'}
        except Exception as e:
            # Log the error but don't crash the rendering
            print(f"Warning: Error rendering field with required attributes: {e}")
            pass
        
        return field


class SafeRequiredWidget(forms.Widget):
    """
    Custom widget that ensures required attributes are always rendered correctly.
    This prevents the "True is not defined" JavaScript error.
    """
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        try:
            # Ensure required attribute is always a string
            if 'required' in attrs and attrs['required'] is True:
                attrs['required'] = 'required'
                attrs['data-required'] = 'true'
        except Exception as e:
            # Log the error but don't crash the widget initialization
            print(f"Warning: Error initializing SafeRequiredWidget: {e}")
            pass
        super().__init__(attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        # Ensure required attribute is always a string
        if attrs and 'required' in attrs and attrs['required'] is True:
            attrs['required'] = 'required'
            attrs['data-required'] = 'true'
        return super().render(name, value, attrs, renderer)


def _inject_spec_fields(form_obj: forms.ModelForm):
    """
    Dynamically inject fields from FORMS_SPEC into forms.
    This allows forms to have extra fields not defined in Django models.
    """
    if not FORMS_SPEC:
        return
    
    try:
        # Get the model name from the form's Meta class
        model_name = form_obj.Meta.model.__name__
        
        if model_name not in FORMS_SPEC:
            return
        
        spec = FORMS_SPEC[model_name]
        
        # Process each section in the spec
        for section_name, fields in spec.get("sections", {}).items():
            for field_spec in fields:
                fname = field_spec.get("name")
                ftype = field_spec.get("type")
                fdefault = field_spec.get("default")
                frequired = field_spec.get("required", False)
                
                if not fname or fname in form_obj.fields:
                    continue
                
                # Create the appropriate field type
                if ftype == "char":
                    field = forms.CharField(
                        max_length=255,
                        required=frequired,
                        initial=fdefault,
                        widget=forms.TextInput(attrs={"class": "form-control"})
                    )
                elif ftype == "int":
                    field = forms.IntegerField(
                        required=frequired,
                        initial=fdefault,
                        widget=forms.NumberInput(attrs={"class": "form-control"})
                    )
                elif ftype == "decimal":
                    field = forms.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        required=frequired,
                        initial=fdefault,
                        widget=forms.NumberInput(attrs={"class": "form-control"})
                    )
                elif ftype == "date":
                    field = forms.DateField(
                        required=frequired,
                        initial=fdefault,
                        widget=forms.DateInput(attrs={
                            "class": "form-control date-field",
                            "type": "date",
                            "data-flatpickr": "true"
                        })
                    )
                elif ftype == "boolean":
                    choices = field_spec.get("choices", [("True", "Yes"), ("False", "No")])
                    field = forms.ChoiceField(
                        choices=choices,
                        required=frequired,
                        initial=str(fdefault) if fdefault is not None else None,
                        widget=forms.Select(attrs={"class": "form-control"})
                    )
                    print(f"DEBUG: _inject_spec_fields - Creating boolean select field: {fname} with choices: {field_spec.get('choices')}")
                elif ftype == "file":
                    field = forms.FileField(
                        required=frequired,
                        widget=forms.FileInput(attrs={"class": "form-control"})
                    )
                elif ftype == "image":
                    field = forms.ImageField(
                        required=frequired,
                        widget=forms.FileInput(attrs={
                            "class": "form-control",
                            "accept": "image/*"
                        })
                    )
                elif ftype == "foreign_key":
                    model_name = field_spec.get("model")
                    if model_name:
                        try:
                            model_class = globals().get(model_name)
                            if model_class:
                                field = forms.ModelChoiceField(
                                    queryset=model_class.objects.all(),
                                    required=frequired,
                                    widget=forms.Select(attrs={"class": "form-control"})
                                )
                        except Exception:
                            continue
                
                # Add the field to the form if it was created
                if 'field' in locals():
                    form_obj.fields[fname] = field
                    print(f"DEBUG: _inject_spec_fields - Added field {fname} of type {ftype} to {form_obj.__class__.__name__}")
                    print(f"DEBUG: Field {fname} initial value: {field.initial}")
                    print(f"DEBUG: Field {fname} required: {field.required}")
        
        # After injecting all spec fields, prefill them with data from extra_data
        if hasattr(form_obj, '_prefill_extra_fields'):
            form_obj._prefill_extra_fields()
    
    except Exception as e:
        # Log the error but don't crash the form injection
        print(f"Warning: Error injecting spec fields for {form_obj.__class__.__name__}: {e}")
        pass


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
    """
    Base form that excludes raw CSV data fields and handles extra_data properly.
    """
    
    class Meta:
        exclude = [
            "raw_csv_data", "extra_data", "created_at", "updated_at",
            "created_by", "updated_by", "is_active", "is_deleted"
        ]

    def __init__(self, *args, **kwargs):
        # Extract extra_fields before calling super().__init__
        self.extra_fields = kwargs.pop('extra_fields', None)
        super().__init__(*args, **kwargs)
        
        # Apply required attribute fixes
        fix_required_attributes(self)
    
    def _prefill_extra_fields(self):
        """Prefill fields from instance.extra_data on EDIT - called after _inject_spec_fields"""
        try:
            instance = getattr(self, "instance", None)
            if instance and getattr(instance, "pk", None):
                model_field_names = {getattr(ff, "name", "") for ff in instance._meta.get_fields()}
                extra = (getattr(instance, "extra_data", {}) or {}).copy()
                
                print(f"DEBUG: _prefill_extra_fields - Instance extra_data: {extra}")
                print(f"DEBUG: _prefill_extra_fields - Model field names: {model_field_names}")
                
                # Prefill non-model fields from extra_data
                for field_name, field in self.fields.items():
                    if field_name not in model_field_names and field_name in extra:
                        field.initial = extra[field_name]
                        print(f"DEBUG: Prefilled field '{field_name}' with value: {extra[field_name]}")
                    elif field_name in extra:
                        # Also check for fields that might be in extra_data
                        field.initial = extra[field_name]
                        print(f"DEBUG: Prefilled model field '{field_name}' with value: {extra[field_name]}")
        except Exception as e:
            print(f"Warning: Error prefilling fields from extra_data: {e}")
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Note: We're not processing extra_data here anymore since the view handles it
        # This prevents conflicts between form processing and view processing
        print(f"DEBUG: {self.__class__.__name__} clean() - cleaned_data keys: {list(cleaned_data.keys())}")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Note: extra_data is handled by the view, not here
        print(f"DEBUG: {self.__class__.__name__} save() - instance extra_data: {getattr(instance, 'extra_data', None)}")
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance
    
    def __str__(self):
        """Ensure required attributes are fixed before rendering"""
        try:
            fix_required_attributes(self)
        except Exception as e:
            print(f"Warning: Error fixing required attributes in __str__ for {self.__class__.__name__}: {e}")
        return super().__str__()
    
    def __html__(self):
        """Ensure required attributes are fixed before rendering"""
        try:
            fix_required_attributes(self)
        except Exception as e:
            print(f"Warning: Error fixing required attributes in __html__ for {self.__class__.__name__}: {e}")
        return super().__str__()


class CompanyForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Company
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class BranchForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Branch
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)

        # Set help_text for open_date to empty string to prevent duplication
        if 'open_date' in self.fields:
            self.fields['open_date'].help_text = ''
        
        # Set initial value for export_flag
        if 'export_flag' in self.fields:
            self.fields['export_flag'].initial = False

    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure export_flag has a default value
        if 'export_flag' not in cleaned_data:
            cleaned_data['export_flag'] = False
        
        return cleaned_data
    
    def __str__(self):
        """Ensure required attributes are fixed before rendering"""
        fix_required_attributes(self)
        return super().__str__()
    
    def __html__(self):
        """Ensure required attributes are fixed before rendering"""
        fix_required_attributes(self)
        return super().__str__()


class VillageForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Village
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class CenterForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Center
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class GroupForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Group
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class RoleForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Role
        exclude = ExcludeRawCSVDataForm.Meta.exclude + ["permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class UserCreationForm(ExcludeRawCSVDataForm):
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
    
    is_reports = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input",
        }),
        label="Is Reports",
    )
    
    is_staff = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input",
        }),
        label="Is Staff",
    )

    class Meta(ExcludeRawCSVDataForm.Meta):
        model = UserCreation
        fields = [
            "staff", "password", "full_name", "branch", "department", "mobile", "status", "is_reports", "is_staff"
        ]
        exclude = ["user"]  # user handled manually

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inject spec fields first
        _inject_spec_fields(self)

        # Set required fields
        if 'full_name' in self.fields:
            self.fields['full_name'].required = True
        if 'staff' in self.fields:
            self.fields['staff'].required = True

        # Set up staff queryset - simplified and more efficient
        try:
            # Use a simple, fast query without complex filtering
            staff_qs = Staff.objects.filter(
                status="active"
            ).exclude(
                staffcode__isnull=True
            ).exclude(
                staffcode=""
            ).order_by("name", "staffcode")[:100]  # Limit to 100 for performance
            
            if staff_qs.exists():
                self.fields["staff"].queryset = staff_qs
                print(f"✅ UserCreationForm: Loaded {staff_qs.count()} active staff")
            else:
                # If no active staff, show all staff
                all_staff = Staff.objects.all()[:100]
                self.fields["staff"].queryset = all_staff
                print(f"⚠️ UserCreationForm: No active staff found, showing {all_staff.count()} total staff")
                
        except Exception as e:
            # Fallback to empty queryset if there's an error
            print(f"❌ UserCreationForm: Error loading staff: {e}")
            self.fields["staff"].queryset = Staff.objects.none()
        
        # Set up branch queryset - simplified
        try:
            from .models import Branch
            branch_qs = Branch.objects.filter(
                status="active"
            ).order_by("name")[:50]  # Limit to 50 for performance
            
            if branch_qs.exists():
                self.fields["branch"].queryset = branch_qs
                print(f"✅ UserCreationForm: Loaded {branch_qs.count()} active branches")
            else:
                # If no active branches, show all branches
                all_branches = Branch.objects.all()[:50]
                self.fields["branch"].queryset = all_branches
                print(f"⚠️ UserCreationForm: No active branches found, showing {all_branches.count()} total branches")
                
        except Exception as e:
            # Fallback to empty queryset if there's an error
            print(f"❌ UserCreationForm: Error loading branches: {e}")
            self.fields["branch"].queryset = Branch.objects.none()


class UserPermissionForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = UserPermission
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class StaffForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Staff
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inject spec fields first
        _inject_spec_fields(self)
        
        # Set querysets for foreign key fields to show only active records
        try:
            from .models import Branch, Cadre
            
            # Set branch field queryset to show only active branches
            if "branch" in self.fields:
                self.fields["branch"] = forms.ModelChoiceField(
                    queryset=Branch.objects.filter(status="active").order_by("name"),
                    required=False,
                    widget=forms.Select(attrs={"class": "form-control"}),
                    label="Branch"
                )
                print(f"DEBUG: Forced branch field to ModelChoiceField with {self.fields['branch'].queryset.count()} active branches")
        
            # Set cadre field queryset to show only active cadres
            if "cadre" in self.fields:
                self.fields["cadre"] = forms.ModelChoiceField(
                    queryset=Cadre.objects.filter(status="active").order_by("name"),
                    required=False,
                    widget=forms.Select(attrs={"class": "form-control"}),
                    label="Cadre"
                )
                print(f"DEBUG: Forced cadre field to ModelChoiceField with {self.fields['cadre'].queryset.count()} active cadres")
        except Exception as e:
            print(f"DEBUG: Error setting foreign key fields: {e}")
        
        # Make joining_date read-only for new records
        if not self.instance.pk and "joining_date" in self.fields:
            self.fields["joining_date"].widget.attrs["readonly"] = "readonly"
            print(f"DEBUG: Made joining_date field read-only for new record")
        

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
            clean_emergency_contact = str(emergency_contact).replace(" ", "")
            if not clean_emergency_contact.isdigit() or len(clean_emergency_contact) != 10:
                print(f"DEBUG: Emergency contact validation failed in clean method")
                self.add_error("extra__emergency_contact", "Emergency contact must be exactly 10 digits")
            else:
                cleaned_data["extra__emergency_contact"] = clean_emergency_contact
                print(f"DEBUG: Emergency contact validation passed, cleaned: {clean_emergency_contact}")

        return cleaned_data

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class PrepaidForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Prepaid
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class MortgageForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Mortgage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class ExSavingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = ExSaving
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class DisbursementForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Disbursement
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class LoanApprovalForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanApproval
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class ClientForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Client
        fields = [
            "smtcode", "name", "group", "gender", "aadhar", "contactno", 
            "join_date", "status"
        ]
    
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
            clean_aadhaar = str(aadhar).replace(" ", "")
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
        
        # Inject spec fields first
        _inject_spec_fields(self)
        
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


# ─────────  ADDITIONAL IMPORTANT MODEL FORMS  ─────────

class LoanApplicationForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanApplication
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class FieldScheduleForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = FieldSchedule
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class FieldReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = FieldReport
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class WeeklyReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = WeeklyReport
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class MonthlyReportForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = MonthlyReport
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class BusinessSettingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = BusinessSetting
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class AccountHeadForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = AccountHead
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class VoucherForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Voucher
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class PostingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Posting
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class RecoveryPostingForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = RecoveryPosting
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class AppointmentForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Appointment
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class SalaryStatementForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = SalaryStatement
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class PaymentForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Payment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class RepaymentForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Repayment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class LoanRestructureForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = LoanRestructure
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class NotificationForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Notification
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class GatewayEventForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = GatewayEvent
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class EWIFlagForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = EWIFlag
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class KYCDocumentForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = KYCDocument
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class AlertRuleForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = AlertRule
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class ColumnForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Column
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


class CadreForm(ExcludeRawCSVDataForm):
    class Meta(ExcludeRawCSVDataForm.Meta):
        model = Cadre
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)


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
    Smtavail, Temp
]

for model_cls in _csv_models:
    form_name = f"{model_cls.__name__}Form"
    meta_cls = type("Meta", (ExcludeRawCSVDataForm.Meta,), {
        "model": model_cls,
        "fields": "__all__"
    })
    
    # Create form class with _inject_spec_fields in __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _inject_spec_fields(self)
    
    globals()[form_name] = type(form_name, (ExcludeRawCSVDataForm,), {
        "Meta": meta_cls,
        "__init__": __init__
    })
