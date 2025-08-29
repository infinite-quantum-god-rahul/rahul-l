# companies/api_serializers.py
from rest_framework import serializers
from django.conf import settings
from .models import Client, Staff, Company

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
