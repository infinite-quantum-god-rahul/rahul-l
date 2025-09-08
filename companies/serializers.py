from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Branch, Staff, Users, UserPermission, Company, Village, Center, 
    Group, Fund, LoanCols, AccFundLoanCols, AccFundLoans, 
    AccountHead, Voucher, Posting, Payment, Repayment, RecoveryPosting,
    EquityShare, EquityShare2, EquityShare31032014, EquityShare31032015,
    DayEnd, CollectionReport, Cheque, Arrear, AccountMaster, 
    AccountCashbook, AccountCashbookOld, AccHeads, Codes, Contacts,
    Cobarower, GR, CollectionRpt
)
from .models_sml import (
    Client, LoanApplication, LoanSchedule, DisbursementRecord, 
    LoanCollection, FieldSchedule, FieldVisit, NPAAccount, 
    KYCDocument, CreditReport, LoanRestructuring, SMLConfiguration,
    LoanTypeConfiguration, SMLLog, SMLAuditTrail
)


# Core SML Models Serializers
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class LoanApplicationSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    loan_type_name = serializers.CharField(source='loan_type.name', read_only=True)
    
    class Meta:
        model = LoanApplication
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class LoanScheduleSerializer(serializers.ModelSerializer):
    loan_application_ref = serializers.CharField(source='loan_application.loan_number', read_only=True)
    
    class Meta:
        model = LoanSchedule
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FieldScheduleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    village_name = serializers.CharField(source='village.name', read_only=True)
    
    class Meta:
        model = FieldSchedule
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class FieldVisitSerializer(serializers.ModelSerializer):
    field_schedule_ref = serializers.CharField(source='field_schedule.reference_number', read_only=True)
    
    class Meta:
        model = FieldVisit
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class NPAAccountSerializer(serializers.ModelSerializer):
    loan_application_ref = serializers.CharField(source='loan_application.loan_number', read_only=True)
    
    class Meta:
        model = NPAAccount
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class KYCDocumentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    
    class Meta:
        model = KYCDocument
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class CreditReportSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    
    class Meta:
        model = CreditReport
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


# Existing Models Serializers
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class StaffSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class UsersSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserPermissionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user_profile.full_name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = UserPermission
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class CenterSerializer(serializers.ModelSerializer):
    village_name = serializers.CharField(source='village.name', read_only=True)
    
    class Meta:
        model = Center
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class GroupSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


# Financial Models Serializers
class AccountHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHead
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


# Dashboard Statistics Serializer
class DashboardStatsSerializer(serializers.Serializer):
    total_clients = serializers.IntegerField()
    total_loans = serializers.IntegerField()
    total_disbursed = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_collected = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_npa = serializers.DecimalField(max_digits=15, decimal_places=2)
    active_field_schedules = serializers.IntegerField()
    pending_kyc = serializers.IntegerField()
    overdue_loans = serializers.IntegerField()


# Search Serializer
class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)
    entity_type = serializers.CharField(max_length=50, required=False)
    limit = serializers.IntegerField(default=20)


# User Authentication Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    role_flags = serializers.DictField(read_only=True)

