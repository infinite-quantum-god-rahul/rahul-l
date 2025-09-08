"""
SML777 Ultra Minimal URL Configuration
=====================================

The most basic URL configuration possible.
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponse

def home_view(request):
    """Beautiful home page view"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SML777 - Company Management System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 600px;
                width: 90%;
            }
            
            .logo {
                font-size: 48px;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 20px;
            }
            
            .title {
                font-size: 32px;
                color: #333;
                margin-bottom: 10px;
            }
            
            .subtitle {
                font-size: 18px;
                color: #666;
                margin-bottom: 30px;
            }
            
            .status {
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                font-weight: bold;
            }
            
            .buttons {
                display: flex;
                gap: 15px;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 30px;
            }
            
            .btn {
                background: #667eea;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s ease;
                display: inline-block;
            }
            
            .btn:hover {
                background: #5a6fd8;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            
            .btn-secondary {
                background: #6c757d;
            }
            
            .btn-secondary:hover {
                background: #5a6268;
            }
            
            .features {
                margin-top: 30px;
                text-align: left;
            }
            
            .feature {
                display: flex;
                align-items: center;
                margin: 10px 0;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 8px;
            }
            
            .feature-icon {
                font-size: 20px;
                margin-right: 10px;
            }
            
            .footer {
                margin-top: 30px;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🏢 SML777</div>
            <h1 class="title">Company Management System</h1>
            <p class="subtitle">Professional Business Management Platform</p>
            
            <div class="status">
                ✅ System Online - All Services Running
            </div>
            
            <div class="buttons">
                <a href="/admin/" class="btn">Admin Panel</a>
                <a href="/health/" class="btn btn-secondary">System Status</a>
                <a href="/html/" class="btn btn-secondary">Simple View</a>
            </div>
            
            <div class="features">
                <h3 style="text-align: center; margin-bottom: 20px; color: #333;">System Features</h3>
                <div class="feature">
                    <span class="feature-icon">👥</span>
                    <span>User Management</span>
                </div>
                <div class="feature">
                    <span class="feature-icon">🏢</span>
                    <span>Company Management</span>
                </div>
                <div class="feature">
                    <span class="feature-icon">📊</span>
                    <span>Dashboard & Analytics</span>
                </div>
                <div class="feature">
                    <span class="feature-icon">🔐</span>
                    <span>Secure Authentication</span>
                </div>
                <div class="feature">
                    <span class="feature-icon">☁️</span>
                    <span>Cloud Hosted on Render</span>
                </div>
            </div>
            
            <div class="footer">
                <p>🚀 Powered by Django & Render.com</p>
                <p>Version: Ultra-Minimal 1.0 | Status: Production Ready</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

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

def json_view(request):
    """JSON API endpoint"""
    return JsonResponse({
        'message': 'SML777 is working!',
        'status': 'success',
        'version': 'ultra-minimal-1.0',
        'endpoints': {
            'home': '/',
            'admin': '/admin/',
            'health': '/health/',
            'json': '/json/',
            'html': '/html/'
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_view, name='health'),
    path('json/', json_view, name='json'),
    path('html/', simple_html, name='html'),
    path('', home_view, name='home'),
]
