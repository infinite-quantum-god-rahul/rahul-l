# companies/models_sml.py
# SML Project Models
# Integrates with existing Django system
# Preserves all existing functionality

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Import existing models
from .models import Branch, Company

# ========================================
# SML PROJECT CORE MODELS
# ========================================

class SMLClient(models.Model):
    """SML Client/Customer Model - Enhanced version"""
    
    # Basic Information
    full_name = models.CharField(max_length=255)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    
    # Address Information
    address = models.TextField()
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    
    # Personal Information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    occupation = models.CharField(max_length=100)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Business Information
    business_type = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    business_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # KYC Status
    kyc_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected')
    ], default='pending')
    
    # System Fields
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted')
    ], default='active')
    
    # Relationships
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sml_clients')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_clients'
        verbose_name = 'SML Client'
        verbose_name_plural = 'SML Clients'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.aadhaar_number})"
    
    @property
    def age(self):
        """Calculate client age"""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

class SMLLoanApplication(models.Model):
    """SML Loan Application Model - Enhanced version"""
    
    # Application Information
    application_id = models.CharField(max_length=20, unique=True)
    loan_type = models.CharField(max_length=50, choices=[
        ('personal', 'Personal Loan'),
        ('business', 'Business Loan'),
        ('agriculture', 'Agriculture Loan'),
        ('gold', 'Gold Loan'),
        ('vehicle', 'Vehicle Loan'),
        ('home', 'Home Loan'),
        ('education', 'Education Loan')
    ])
    
    # Loan Details
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tenure_months = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Application Status
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('closed', 'Closed')
    ], default='draft')
    
    # Relationships
    client = models.ForeignKey(SMLClient, on_delete=models.CASCADE, related_name='loan_applications')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sml_loans')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_loan_applications'
        verbose_name = 'SML Loan Application'
        verbose_name_plural = 'SML Loan Applications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application_id} - {self.client.full_name}"

class SMLLoanSchedule(models.Model):
    """SML Loan Schedule/EMI Model"""
    
    loan_application = models.ForeignKey(SMLLoanApplication, on_delete=models.CASCADE, related_name='schedules')
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2)
    principal_component = models.DecimalField(max_digits=12, decimal_places=2)
    interest_component = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Payment Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('partial', 'Partial')
    ], default='pending')
    
    # Payment Details
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_date = models.DateField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_loan_schedules'
        verbose_name = 'SML Loan Schedule'
        verbose_name_plural = 'SML Loan Schedules'
        ordering = ['loan_application', 'installment_number']
    
    def __str__(self):
        return f"{self.loan_application.application_id} - EMI {self.installment_number}"

class SMLDisbursementRecord(models.Model):
    """SML Loan Disbursement Record"""
    
    loan_application = models.ForeignKey(SMLLoanApplication, on_delete=models.CASCADE, related_name='disbursements')
    disbursement_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    disbursement_method = models.CharField(max_length=50, choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('cash', 'Cash'),
        ('upi', 'UPI')
    ])
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_disbursement_records'
        verbose_name = 'SML Disbursement Record'
        verbose_name_plural = 'SML Disbursement Records'
        ordering = ['-disbursement_date']
    
    def __str__(self):
        return f"{self.loan_application.application_id} - {self.amount}"

class SMLLoanCollection(models.Model):
    """SML Loan Collection/Payment Record"""
    
    loan_application = models.ForeignKey(SMLLoanApplication, on_delete=models.CASCADE, related_name='collections')
    collection_date = models.DateField()
    amount_collected = models.DecimalField(max_digits=12, decimal_places=2)
    collection_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('auto_debit', 'Auto Debit')
    ])
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_loan_collections'
        verbose_name = 'SML Loan Collection'
        verbose_name_plural = 'SML Loan Collections'
        ordering = ['-collection_date']
    
    def __str__(self):
        return f"{self.loan_application.application_id} - {self.amount_collected}"

class SMLFieldSchedule(models.Model):
    """SML Field Schedule for Staff"""
    
    reference_number = models.CharField(max_length=50, unique=True)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='field_schedules')
    village = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    purpose = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed')
    ], default='scheduled')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_field_schedules'
        verbose_name = 'SML Field Schedule'
        verbose_name_plural = 'SML Field Schedules'
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.reference_number} - {self.staff.name}"

class SMLFieldVisit(models.Model):
    """SML Field Visit Record"""
    
    field_schedule = models.ForeignKey(SMLFieldSchedule, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField()
    visit_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    
    # Visit Details
    purpose_achieved = models.BooleanField(default=False)
    findings = models.TextField(blank=True, null=True)
    next_action_required = models.TextField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='scheduled')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_field_visits'
        verbose_name = 'SML Field Visit'
        verbose_name_plural = 'SML Field Visits'
        ordering = ['-visit_date']
    
    def __str__(self):
        return f"{self.field_schedule.reference_number} - {self.visit_date}"

class SMLNPAAccount(models.Model):
    """SML NPA (Non-Performing Asset) Account"""
    
    loan_application = models.ForeignKey(SMLLoanApplication, on_delete=models.CASCADE, related_name='npa_accounts')
    npa_date = models.DateField()
    outstanding_amount = models.DecimalField(max_digits=15, decimal_places=2)
    days_past_due = models.PositiveIntegerField()
    
    # NPA Category
    npa_category = models.CharField(max_length=20, choices=[
        ('sub_standard', 'Sub-Standard'),
        ('doubtful', 'Doubtful'),
        ('loss', 'Loss')
    ])
    
    # Recovery Status
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('under_recovery', 'Under Recovery'),
        ('settled', 'Settled'),
        ('written_off', 'Written Off')
    ], default='active')
    
    # Recovery Details
    recovery_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_recovery_date = models.DateField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_npa_accounts'
        verbose_name = 'SML NPA Account'
        verbose_name_plural = 'SML NPA Accounts'
        ordering = ['-npa_date']
    
    def __str__(self):
        return f"{self.loan_application.application_id} - {self.outstanding_amount}"

class SMLKYCDocument(models.Model):
    """SML KYC Document Management"""
    
    client = models.ForeignKey(SMLClient, on_delete=models.CASCADE, related_name='kyc_documents')
    document_type = models.CharField(max_length=50, choices=[
        ('aadhaar', 'Aadhaar Card'),
        ('pan', 'PAN Card'),
        ('passport', 'Passport'),
        ('driving_license', 'Driving License'),
        ('voter_id', 'Voter ID'),
        ('bank_statement', 'Bank Statement'),
        ('salary_slip', 'Salary Slip'),
        ('income_certificate', 'Income Certificate'),
        ('address_proof', 'Address Proof'),
        ('other', 'Other')
    ])
    
    document_number = models.CharField(max_length=100, blank=True, null=True)
    document_file = models.FileField(upload_to='kyc_documents/', blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    # Verification Status
    verification_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired')
    ], default='pending')
    
    # Verification Details
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verification_date = models.DateField(blank=True, null=True)
    verification_remarks = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_kyc_documents'
        verbose_name = 'SML KYC Document'
        verbose_name_plural = 'SML KYC Documents'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client.full_name} - {self.document_type}"

class SMLCreditReport(models.Model):
    """SML Credit Report Integration"""
    
    client = models.ForeignKey(SMLClient, on_delete=models.CASCADE, related_name='credit_reports')
    credit_bureau = models.CharField(max_length=50, choices=[
        ('cibil', 'CIBIL'),
        ('experian', 'Experian'),
        ('equifax', 'Equifax'),
        ('high_mark', 'High Mark')
    ])
    
    # Credit Score
    credit_score = models.PositiveIntegerField(blank=True, null=True)
    score_range = models.CharField(max_length=20, blank=True, null=True)
    
    # Report Details
    report_date = models.DateField()
    report_file = models.FileField(upload_to='credit_reports/', blank=True, null=True)
    report_summary = models.TextField(blank=True, null=True)
    
    # Risk Assessment
    risk_category = models.CharField(max_length=20, choices=[
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('very_high', 'Very High Risk')
    ], blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_credit_reports'
        verbose_name = 'SML Credit Report'
        verbose_name_plural = 'SML Credit Reports'
        ordering = ['-report_date']
    
    def __str__(self):
        return f"{self.client.full_name} - {self.credit_bureau}"

class SMLLoanRestructuring(models.Model):
    """SML Loan Restructuring"""
    
    loan_application = models.ForeignKey(SMLLoanApplication, on_delete=models.CASCADE, related_name='restructurings')
    restructuring_date = models.DateField()
    original_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    restructured_amount = models.DecimalField(max_digits=15, decimal_places=2)
    new_tenure_months = models.PositiveIntegerField()
    new_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    new_emi_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Restructuring Reason
    reason = models.TextField()
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approval_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('implemented', 'Implemented')
    ], default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_loan_restructurings'
        verbose_name = 'SML Loan Restructuring'
        verbose_name_plural = 'SML Loan Restructurings'
        ordering = ['-restructuring_date']
    
    def __str__(self):
        return f"{self.loan_application.application_id} - Restructuring"

class SMLConfiguration(models.Model):
    """SML System Configuration"""
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_configurations'
        verbose_name = 'SML Configuration'
        verbose_name_plural = 'SML Configurations'
        ordering = ['key']
    
    def __str__(self):
        return f"{self.key}: {self.value}"

class SMLLoanTypeConfiguration(models.Model):
    """SML Loan Type Configuration"""
    
    loan_type = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # Configuration
    min_amount = models.DecimalField(max_digits=15, decimal_places=2)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2)
    min_tenure = models.PositiveIntegerField()
    max_tenure = models.PositiveIntegerField()
    interest_rate_range_min = models.DecimalField(max_digits=5, decimal_places=2)
    interest_rate_range_max = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Requirements
    required_documents = models.JSONField(default=list, blank=True)
    eligibility_criteria = models.JSONField(default=dict, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sml_loan_type_configurations'
        verbose_name = 'SML Loan Type Configuration'
        verbose_name_plural = 'SML Loan Type Configurations'
        ordering = ['loan_type']
    
    def __str__(self):
        return f"{self.name} ({self.loan_type})"

class SMLLog(models.Model):
    """SML System Log"""
    
    level = models.CharField(max_length=20, choices=[
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical')
    ])
    
    message = models.TextField()
    module = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Additional Data
    extra_data = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sml_logs'
        verbose_name = 'SML Log'
        verbose_name_plural = 'ML Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.level}: {self.message[:50]}"

class SMLAuditTrail(models.Model):
    """SML Audit Trail"""
    
    action = models.CharField(max_length=50, choices=[
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('export', 'Export'),
        ('import', 'Import')
    ])
    
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Changes
    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    
    # Additional Info
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sml_audit_trails'
        verbose_name = 'SML Audit Trail'
        verbose_name_plural = 'SML Audit Trails'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action} on {self.model_name} #{self.object_id}"
