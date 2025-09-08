# companies/api_serializers.py
from rest_framework import serializers
from django.conf import settings
from .models import Client, Staff, Company
# Import SML models for new serializers
from .models_sml import (
    SMLClient, SMLLoanApplication, SMLLoanSchedule, SMLDisbursementRecord, 
    SMLLoanCollection, SMLFieldSchedule, SMLFieldVisit, SMLNPAAccount, 
    SMLKYCDocument, SMLCreditReport, SMLLoanRestructuring, SMLConfiguration,
    SMLLoanTypeConfiguration, SMLLog, SMLAuditTrail
)

_IMG_CANDIDATES = ("photo", "image", "picture", "avatar", "logo")

def _first_image_field(obj):
    # 1) named candidates first
    for nm in _IMG_CANDIDATES:
        if hasattr(obj, nm):
            return nm
    # 2) any Image/File field
    try:
        for f in obj._meta.get_fields():
            if getattr(f, "upload_to", None):
                return f.name
    except Exception:
        pass
    return None

def _abs_url(request, f):
    try:
        if not f:
            return None
        url = getattr(f, "url", None) or str(f)
        if not url:
            return None
        if request:
            return request.build_absolute_uri(url)
        return url
    except Exception:
        return None

# ========================================
# EXISTING SERIALIZERS - PRESERVED AS IS
# ========================================

class ClientSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = ["id", "code", "name", "mobile", "photo_url"]

    def get_photo_url(self, obj):
        fld = _first_image_field(obj)
        return _abs_url(self.context.get("request"), getattr(obj, fld, None)) if fld else None

class StaffSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    class Meta:
        model = Staff
        fields = ["id", "code", "name", "mobile", "photo_url"]

    def get_photo_url(self, obj):
        fld = _first_image_field(obj)
        return _abs_url(self.context.get("request"), getattr(obj, fld, None)) if fld else None

class CompanySerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ["id", "code", "name", "logo_url"]

    def get_logo_url(self, obj):
        fld = _first_image_field(obj)
        return _abs_url(self.context.get("request"), getattr(obj, fld, None)) if fld else None

# ========================================
# NEW SML PROJECT SERIALIZERS
# ========================================

class SMLClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMLClient
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLLoanApplicationSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    loan_type_name = serializers.CharField(source='loan_type', read_only=True)
    
    class Meta:
        model = SMLLoanApplication
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLLoanScheduleSerializer(serializers.ModelSerializer):
    loan_application_ref = serializers.CharField(source='loan_application.application_id', read_only=True)
    
    class Meta:
        model = SMLLoanSchedule
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLFieldScheduleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    village_name = serializers.CharField(source='village', read_only=True)
    
    class Meta:
        model = SMLFieldSchedule
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLFieldVisitSerializer(serializers.ModelSerializer):
    field_schedule_ref = serializers.CharField(source='field_schedule.reference_number', read_only=True)
    
    class Meta:
        model = SMLFieldVisit
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLNPAAccountSerializer(serializers.ModelSerializer):
    loan_application_ref = serializers.CharField(source='loan_application.application_id', read_only=True)
    
    class Meta:
        model = SMLNPAAccount
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLKYCDocumentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    
    class Meta:
        model = SMLKYCDocument
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLCreditReportSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    
    class Meta:
        model = SMLCreditReport
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLLoanRestructuringSerializer(serializers.ModelSerializer):
    loan_application_ref = serializers.CharField(source='loan_application.application_id', read_only=True)
    
    class Meta:
        model = SMLLoanRestructuring
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMLConfiguration
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SMLLoanTypeConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMLLoanTypeConfiguration
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


# User Profile Serializer
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
