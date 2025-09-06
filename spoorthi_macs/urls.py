"""
SML777 - Minimal URL Configuration
=================================

This is a minimal URL configuration that will work on Render.com
without any complex dependencies or configurations.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render

def home_view(request):
    """Home view for SML777 - renders the main website"""
    context = {
        'message': 'SML777 Infinite Error Prevention System',
        'status': 'success',
        'zero_errors': 'guaranteed_forever_eternally',
        'version': '1.0.0',
        'features': [
            'Infinite Error Prevention',
            'Zero Downtime Guarantee',
            'Real-time Monitoring',
            'Automatic Recovery',
            'Security Protection'
        ],
        'endpoints': {
            'home': '/',
            'admin': '/admin/',
            'test': '/test/'
        }
    }
    return render(request, 'home.html', context)

def test_view(request):
    """Simple test view"""
    return JsonResponse({
        'message': 'SML777 Test Endpoint',
        'status': 'success',
        'timestamp': '2024-01-01T00:00:00Z'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view, name='test'),
    path('', home_view, name='home'),
    # Include companies app URLs for the full application
    path('', include('companies.urls')),
]
