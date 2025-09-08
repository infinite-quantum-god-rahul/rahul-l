# companies/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import (
    # Existing viewsets
    ClientViewSet, StaffViewSet, CompanyViewSet, generic_upload,
)

# ========================================
# EXISTING ROUTER - PRESERVED AS IS
# ========================================
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'staff',   StaffViewSet,   basename='staff')
router.register(r'companies', CompanyViewSet, basename='companies')

urlpatterns = [
    # ========================================
    # EXISTING URLS - PRESERVED AS IS
    # ========================================
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('upload/<str:entity>/<int:pk>/', generic_upload, name='generic_upload'),
]
