# companies/api_views.py
from django.apps import apps
from django.db import transaction
from django.db.models import Model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Client, Staff, Company
from .api_serializers import ClientSerializer, StaffSerializer, CompanySerializer

IMG_PARAM_NAMES = ("photo", "image", "file", "picture", "avatar", "logo")
IMG_FIELD_CANDIDATES = ("photo", "image", "picture", "avatar", "logo")

def _first_image_field_on_model(obj: Model):
    # prefer conventional names
    for nm in IMG_FIELD_CANDIDATES:
        if hasattr(obj, nm):
            return nm
    # fallback to any upload_to field
    try:
        for f in obj._meta.get_fields():
            if getattr(f, "upload_to", None):
                return f.name
    except Exception:
        pass
    return None

class BaseUploadMixin:
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=True, methods=["post"], url_path="upload")
    def upload(self, request, pk=None):
        instance = self.get_object()
        file_obj = None
        for p in IMG_PARAM_NAMES:
            if p in request.FILES:
                file_obj = request.FILES[p]
                break
        if not file_obj:
            return Response({"detail": "File required in one of: " + ", ".join(IMG_PARAM_NAMES)}, status=400)

        fld = _first_image_field_on_model(instance)
        if not fld:
            return Response({"detail": "No image field found on model"}, status=400)

        with transaction.atomic():
            setattr(instance, fld, file_obj)
            instance.save(update_fields=[fld])

        return Response(self.get_serializer(instance, context={"request": request}).data, status=200)

class ClientViewSet(BaseUploadMixin, viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by("id")
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

class StaffViewSet(BaseUploadMixin, viewsets.ModelViewSet):
    queryset = Staff.objects.all().order_by("id")
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyViewSet(BaseUploadMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by("id")
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def generic_upload(request, entity: str, pk: int):
    Model = apps.get_model("companies", entity) or apps.get_model("companies", entity.capitalize())
    if not Model:
        return Response({"detail": f"Unknown entity {entity}"}, status=404)
    try:
        obj = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        return Response({"detail": "Not found"}, status=404)

    file_obj = None
    for p in IMG_PARAM_NAMES:
        if p in request.FILES:
            file_obj = request.FILES[p]
            break
    if not file_obj:
        return Response({"detail": "File required"}, status=400)

    fld = _first_image_field_on_model(obj)
    if not fld:
        return Response({"detail": "No image/file field on entity"}, status=400)

    with transaction.atomic():
        setattr(obj, fld, file_obj)
        obj.save(update_fields=[fld])

    # minimal echo
    try:
        url = request.build_absolute_uri(getattr(getattr(obj, fld), "url", ""))
    except Exception:
        url = None
    return Response({"success": True, "entity": entity, "id": obj.pk, "field": fld, "url": url}, status=200)
