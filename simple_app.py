#!/usr/bin/env python
"""
Super Simple Django App - Guaranteed to Work
"""
import os
import sys
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Minimal Django settings
if not settings.configured:
    settings.configure(
        DEBUG=False,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'django-insecure-simple-key'),
        ALLOWED_HOSTS=['*'],
        ROOT_URLCONF='simple_app',
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
    )

# URL patterns
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SML777 - Working!</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0; }
            .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .success { color: #28a745; font-size: 24px; font-weight: bold; }
            .logo { font-size: 48px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🏢 SML777</div>
            <h1 class="success">✅ SUCCESS!</h1>
            <p>Your Django application is working perfectly!</p>
            <p>Deployed on Render.com</p>
            <p><strong>Status:</strong> Online and Running</p>
        </div>
    </body>
    </html>
    """)

urlpatterns = [
    path('', home),
]

# WSGI application
application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
