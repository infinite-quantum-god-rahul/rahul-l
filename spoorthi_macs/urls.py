"""
SML777 URL Configuration
========================

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import traceback
import sys

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'SML777 Django application is running',
        'debug': settings.DEBUG,
        'database': 'connected' if settings.DATABASES else 'not configured'
    })

def error_debug(request):
    """Debug endpoint to help troubleshoot 500 errors"""
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return JsonResponse({
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'database_status': db_status,
        'static_files': settings.STATIC_URL,
        'media_files': settings.MEDIA_URL,
        'secret_key_set': bool(settings.SECRET_KEY),
        'installed_apps': settings.INSTALLED_APPS,
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('debug/', error_debug, name='error_debug'),
    path('', include('companies.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)