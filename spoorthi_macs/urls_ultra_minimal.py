"""
SML777 Ultra Minimal URL Configuration
=====================================

The most basic URL configuration possible.
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponse

def home_view(request):
    """Ultra simple home view"""
    return JsonResponse({
        'message': 'SML777 is working!',
        'status': 'success',
        'version': 'ultra-minimal-1.0'
    })

def health_view(request):
    """Ultra simple health check"""
    return JsonResponse({'status': 'healthy'})

def simple_html(request):
    """Simple HTML response"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SML777 - Working!</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .success { color: green; font-size: 24px; }
        </style>
    </head>
    <body>
        <h1 class="success">✅ SML777 is Working!</h1>
        <p>Your Django application is successfully deployed on Render.com</p>
        <p><a href="/admin/">Admin Panel</a> | <a href="/health/">Health Check</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_view, name='health'),
    path('html/', simple_html, name='html'),
    path('', home_view, name='home'),
]
