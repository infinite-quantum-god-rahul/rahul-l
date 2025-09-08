"""
SML777 Companies URLs
====================

Simple URL configuration for testing deployment.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Simple test endpoints
    path('', views.simple_home, name='simple_home'),
    path('health/', views.simple_health, name='simple_health'),
    path('test/', views.simple_home, name='test'),
    
    # Existing endpoints (if they exist)
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('admin/', views.admin_dashboard, name='admin_dashboard'),
]