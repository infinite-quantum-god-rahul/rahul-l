# companies/forms_sml.py
# SML Project Forms
# Integrates with existing Django system
# Preserves all existing functionality

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .models_sml import *

# ========================================
# CLIENT MANAGEMENT FORMS
# ========================================

class ClientForm(forms.ModelForm):
    """Client Registration Form"""
    
    # Additional validation fields
    confirm_aadhaar = forms.CharField(max_length=12, label='Confirm Aadhaar Number')
    confirm_contact = forms.CharField(max_length=15, label='Confirm Contact Number')
    
    class Meta:
        model = Client
        fields = [
            'full_name', 'aadhaar_number', 'pan_number', 'contact_number', 'email',
            'address', 'village', 'district', 'state', 'pincode',
            'date_of_birth', 'gender', 'occupation', 'monthly_income',
            'business_type', 'business_address', 'business_income'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name as per Aadhaar'
            }),
            'aadhaar_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12-digit Aadhaar number',
                'pattern': '[0-9]{12}',
                'maxlength': '12'
            }),
            'pan_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-character PAN number',
                'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}',
                'maxlength': '10'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit mobile number',
                'pattern': '[0-9]{10}',
                'maxlength': '10'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address (optional)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
            'village': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter village name'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter district name'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state name'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '6-digit pincode',
                'pattern': '[0-9]{6}',
                'maxlength': '6'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter occupation'
            }),
            'monthly_income': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter monthly income in ₹',
                'min': '0',
                'step': '100'
            }),
            'business_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter business type (if applicable)'
            }),
            'business_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter business address (if applicable)'
            }),
            'business_income': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter business income in ₹ (if applicable)',
                'min': '0',
                'step': '100'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        aadhaar_number = cleaned_data.get('aadhaar_number')
        confirm_aadhaar = cleaned_data.get('confirm_aadhaar')
        contact_number = cleaned_data.get('contact_number')
        confirm_contact = cleaned_data.get('confirm_contact')
        date_of_birth = cleaned_data.get('date_of_birth')
        
        # Validate Aadhaar confirmation
        if aadhaar_number and confirm_aadhaar and aadhaar_number != confirm_aadhaar:
            raise forms.ValidationError("Aadhaar numbers do not match")
        
        # Validate contact confirmation
        if contact_number and confirm_contact and contact_number != confirm_contact:
            raise forms.ValidationError("Contact numbers do not match")
        
        # Validate date of birth (must be at least 18 years old)
        if date_of_birth:
            today = timezone.now().date()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 18:
                raise forms.ValidationError("Client must be at least 18 years old")
        
        return cleaned_data
    
    def clean_aadhaar_number(self):
        aadhaar = self.cleaned_data.get('aadhaar_number')
        if aadhaar and len(aadhaar) != 12:
            raise forms.ValidationError("Aadhaar number must be exactly 12 digits")
        if aadhaar and not aadhaar.isdigit():
            raise forms.ValidationError("Aadhaar number must contain only digits")
        return aadhaar
    
    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if contact and len(contact) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits")
        if contact and not contact.isdigit():
            raise forms.ValidationError("Contact number must contain only digits")
        return contact

class ClientSearchForm(forms.Form):
    """Client Search Form"""
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, Aadhaar, or contact number'
        })
    )
    
    village = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by village'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + Client._meta.get_field('status').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    kyc_status = forms.ChoiceField(
        required=False,
        choices=[('', 'All KYC Statuses')] + Client._meta.get_field('kyc_status').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# ========================================
# LOAN APPLICATION FORMS
# ========================================

class LoanApplicationForm(forms.ModelForm):
    """Loan Application Form"""
    
    # Additional fields for validation
    confirm_loan_amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        label='Confirm Loan Amount'
    )
    
    class Meta:
        model = LoanApplication
        fields = [
            'loan_type', 'loan_amount', 'interest_rate', 'tenure', 'purpose',
            'processing_fee', 'insurance_amount'
        ]
        widgets = {
            'loan_type': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'updateLoanParameters()'
            }),
            'loan_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter loan amount in ₹',
                'min': '1000',
                'step': '1000',
                'onchange': 'calculateEMI()'
            }),
            'interest_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter interest rate (%)',
                'min': '0',
                'max': '100',
                'step': '0.01',
                'onchange': 'calculateEMI()'
            }),
            'tenure': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tenure in months',
                'min': '3',
                'max': '120',
                'onchange': 'calculateEMI()'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the purpose of the loan'
            }),
            'processing_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Processing fee amount',
                'min': '0',
                'step': '100'
            }),
            'insurance_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Insurance amount (if applicable)',
                'min': '0',
                'step': '100'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        loan_amount = cleaned_data.get('loan_amount')
        confirm_loan_amount = cleaned_data.get('confirm_loan_amount')
        interest_rate = cleaned_data.get('interest_rate')
        tenure = cleaned_data.get('tenure')
        
        # Validate loan amount confirmation
        if loan_amount and confirm_loan_amount and loan_amount != confirm_loan_amount:
            raise forms.ValidationError("Loan amounts do not match")
        
        # Validate interest rate
        if interest_rate and (interest_rate < 0 or interest_rate > 100):
            raise forms.ValidationError("Interest rate must be between 0% and 100%")
        
        # Validate tenure
        if tenure and (tenure < 3 or tenure > 120):
            raise forms.ValidationError("Tenure must be between 3 and 120 months")
        
        return cleaned_data
    
    def clean_loan_amount(self):
        amount = self.cleaned_data.get('loan_amount')
        if amount and amount < 1000:
            raise forms.ValidationError("Minimum loan amount is ₹1,000")
        if amount and amount > 10000000:
            raise forms.ValidationError("Maximum loan amount is ₹1,00,00,000")
        return amount

class LoanApprovalForm(forms.Form):
    """Loan Approval Form"""
    
    approval_status = forms.ChoiceField(
        choices=[
            ('approved', 'Approve'),
            ('rejected', 'Reject'),
            ('under_review', 'Under Review')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    approval_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter approval notes or rejection reason'
        })
    )
    
    approved_amount = forms.DecimalField(
        required=False,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Approved loan amount (if different)'
        })
    )
    
    approved_tenure = forms.IntegerField(
        required=False,
        min_value=3,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Approved tenure in months (if different)'
        })
    )
    
    approved_interest_rate = forms.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Approved interest rate % (if different)'
        })
    )

class LoanRestructureForm(forms.ModelForm):
    """Loan Restructuring Form"""
    
    class Meta:
        model = LoanRestructuring
        fields = [
            'restructuring_type', 'new_tenure', 'new_emi', 'reason', 'supporting_documents'
        ]
        widgets = {
            'restructuring_type': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'updateRestructuringFields()'
            }),
            'new_tenure': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'New tenure in months',
                'min': '1',
                'max': '120'
            }),
            'new_emi': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'New EMI amount',
                'min': '0',
                'step': '100'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain the reason for restructuring'
            }),
            'supporting_documents': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            })
        }

# ========================================
# FIELD OPERATIONS FORMS
# ========================================

class FieldScheduleForm(forms.ModelForm):
    """Field Schedule Form"""
    
    class Meta:
        model = FieldSchedule
        fields = [
            'schedule_date', 'start_time', 'end_time', 'route_name', 'village', 'center',
            'group', 'purpose', 'notes', 'assigned_to'
        ]
        widgets = {
            'schedule_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().isoformat()
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'route_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter route name'
            }),
            'village': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter village name'
            }),
            'center': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter center name'
            }),
            'group': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter group name (optional)'
            }),
            'purpose': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter additional notes'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        schedule_date = cleaned_data.get('schedule_date')
        
        # Validate time range
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time")
        
        # Validate schedule date
        if schedule_date and schedule_date < timezone.now().date():
            raise forms.ValidationError("Schedule date cannot be in the past")
        
        return cleaned_data

class FieldVisitForm(forms.ModelForm):
    """Field Visit Form"""
    
    class Meta:
        model = FieldVisit
        fields = [
            'visit_date', 'visit_type', 'visit_notes', 'client_met',
            'latitude', 'longitude'
        ]
        widgets = {
            'visit_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'visit_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'visit_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter visit details and observations'
            }),
            'client_met': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'GPS Latitude',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'GPS Longitude',
                'step': '0.000001'
            })
        }

# ========================================
# KYC DOCUMENT FORMS
# ========================================

class KYCDocumentForm(forms.ModelForm):
    """KYC Document Upload Form"""
    
    class Meta:
        model = KYCDocument
        fields = [
            'document_type', 'document_number', 'document_file'
        ]
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'updateDocumentNumberField()'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document number (optional)'
            }),
            'document_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'onchange': 'validateFileSize(this)'
            })
        }
    
    def clean_document_file(self):
        file = self.cleaned_data.get('document_file')
        if file:
            # Check file size (5MB limit)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 5MB")
            
            # Check file extension
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
            file_extension = file.name.lower()[file.name.rfind('.'):]
            if file_extension not in allowed_extensions:
                raise forms.ValidationError("Only PDF and image files are allowed")
        
        return file

class KYCVerificationForm(forms.Form):
    """KYC Verification Form"""
    
    verification_status = forms.ChoiceField(
        choices=[
            ('verified', 'Verified'),
            ('rejected', 'Rejected')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    verification_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter verification notes or rejection reason'
        })
    )
    
    document_number_verified = forms.BooleanField(
        required=False,
        label='Document number verified'
    )
    
    document_authentic = forms.BooleanField(
        required=False,
        label='Document appears authentic'
    )

# ========================================
# NPA MANAGEMENT FORMS
# ========================================

class NPAAccountForm(forms.ModelForm):
    """NPA Account Form"""
    
    class Meta:
        model = NPAAccount
        fields = [
            'overdue_amount', 'days_overdue', 'npa_category', 'risk_level',
            'recovery_strategy', 'assigned_to'
        ]
        widgets = {
            'overdue_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter overdue amount',
                'min': '0',
                'step': '100'
            }),
            'days_overdue': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter days overdue',
                'min': '1'
            }),
            'npa_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'risk_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'recovery_strategy': forms.Select(attrs={
                'class': 'form-control'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class NPARecoveryForm(forms.Form):
    """NPA Recovery Form"""
    
    recovery_action = forms.ChoiceField(
        choices=[
            ('field_visit', 'Field Visit'),
            ('legal_notice', 'Legal Notice'),
            ('restructuring', 'Loan Restructuring'),
            ('collateral_realization', 'Collateral Realization'),
            ('settlement', 'Settlement'),
            ('written_off', 'Written Off')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    recovery_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter recovery action details'
        })
    )
    
    next_follow_up_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': timezone.now().date().isoformat()
        })
    )
    
    expected_recovery_amount = forms.DecimalField(
        required=False,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Expected recovery amount',
            'min': '0',
            'step': '100'
        })
    )

# ========================================
# CREDIT BUREAU FORMS
# ========================================

class CreditReportForm(forms.Form):
    """Credit Report Request Form"""
    
    client_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    
    report_source = forms.ChoiceField(
        choices=[
            ('cibil', 'CIBIL'),
            ('equifax', 'Equifax'),
            ('experian', 'Experian'),
            ('high_mark', 'High Mark')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    purpose = forms.ChoiceField(
        choices=[
            ('loan_application', 'Loan Application'),
            ('portfolio_review', 'Portfolio Review'),
            ('risk_assessment', 'Risk Assessment'),
            ('compliance', 'Compliance')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    consent_given = forms.BooleanField(
        required=True,
        label='I confirm that the client has given consent for credit report pull'
    )

# ========================================
# FINANCIAL REPORT FORMS
# ========================================

class FinancialReportForm(forms.Form):
    """Financial Report Generation Form"""
    
    report_type = forms.ChoiceField(
        choices=[
            ('portfolio', 'Portfolio Report'),
            ('collection', 'Collection Report'),
            ('disbursement', 'Disbursement Report'),
            ('npa', 'NPA Report'),
            ('profitability', 'Profitability Report')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        required=False,
        empty_label="All Branches",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    export_format = forms.ChoiceField(
        choices=[
            ('pdf', 'PDF'),
            ('excel', 'Excel'),
            ('csv', 'CSV')
        ],
        initial='pdf',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# ========================================
# UTILITY FORMS
# ========================================

class EMICalculatorForm(forms.Form):
    """EMI Calculator Form"""
    
    loan_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1000)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter loan amount',
            'min': '1000',
            'step': '1000',
            'onchange': 'calculateEMI()'
        })
    )
    
    interest_rate = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter interest rate (%)',
            'min': '0',
            'max': '100',
            'step': '0.01',
            'onchange': 'calculateEMI()'
        })
    )
    
    tenure_months = forms.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(120)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tenure in months',
            'min': '3',
            'max': '120',
            'onchange': 'calculateEMI()'
        })
    )

class CreditScoreCalculatorForm(forms.Form):
    """Credit Score Calculator Form"""
    
    monthly_income = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter monthly income',
            'min': '0',
            'step': '1000'
        })
    )
    
    employment_years = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter years of employment',
            'min': '0',
            'step': '0.5'
        })
    )
    
    credit_history_years = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter credit history years',
            'min': '0',
            'step': '0.5'
        })
    )
    
    existing_loans = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter number of existing loans',
            'min': '0'
        })
    )
    
    payment_history = forms.ChoiceField(
        choices=[
            ('excellent', 'Excellent (90-100%)'),
            ('good', 'Good (80-89%)'),
            ('fair', 'Fair (70-79%)'),
            ('poor', 'Poor (60-69%)'),
            ('very_poor', 'Very Poor (<60%)')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# ========================================
# SYSTEM CONFIGURATION FORMS
# ========================================

class SMLConfigurationForm(forms.ModelForm):
    """SML Configuration Form"""
    
    class Meta:
        model = SMLConfiguration
        fields = [
            'config_key', 'config_value', 'config_type', 'description', 'is_active'
        ]
        widgets = {
            'config_key': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter configuration key'
            }),
            'config_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter configuration value'
            }),
            'config_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter configuration description'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

class LoanTypeConfigurationForm(forms.ModelForm):
    """Loan Type Configuration Form"""
    
    class Meta:
        model = LoanTypeConfiguration
        fields = [
            'loan_type', 'display_name', 'description', 'min_amount', 'max_amount',
            'min_tenure', 'max_tenure', 'min_interest_rate', 'max_interest_rate',
            'processing_fee_percentage', 'insurance_required', 'collateral_required',
            'is_active'
        ]
        widgets = {
            'loan_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter loan type code'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter display name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter loan type description'
            }),
            'min_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000'
            }),
            'max_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000'
            }),
            'min_tenure': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '120'
            }),
            'max_tenure': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '120'
            }),
            'min_interest_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'max_interest_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'processing_fee_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'insurance_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'collateral_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        min_amount = cleaned_data.get('min_amount')
        max_amount = cleaned_data.get('max_amount')
        min_tenure = cleaned_data.get('min_tenure')
        max_tenure = cleaned_data.get('max_tenure')
        min_interest_rate = cleaned_data.get('min_interest_rate')
        max_interest_rate = cleaned_data.get('max_interest_rate')
        
        # Validate amount range
        if min_amount and max_amount and min_amount >= max_amount:
            raise forms.ValidationError("Minimum amount must be less than maximum amount")
        
        # Validate tenure range
        if min_tenure and max_tenure and min_tenure >= max_tenure:
            raise forms.ValidationError("Minimum tenure must be less than maximum tenure")
        
        # Validate interest rate range
        if min_interest_rate and max_interest_rate and min_interest_rate >= max_interest_rate:
            raise forms.ValidationError("Minimum interest rate must be less than maximum interest rate")
        
        return cleaned_data


