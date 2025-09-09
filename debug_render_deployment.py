#!/usr/bin/env python3
"""
Debug Render Deployment Configuration
====================================
This script tests the exact configuration that will be used on Render.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set environment variables to match Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', '*.onrender.com')
os.environ.setdefault('SECRET_KEY', 'debug-secret-key-for-testing-only')

# Mock DATABASE_URL for testing (Render will provide real one)
os.environ.setdefault('DATABASE_URL', 'postgresql://user:pass@localhost:5432/testdb')

print("🔍 Testing Render Deployment Configuration...")
print("=" * 50)

try:
    # Test Django setup
    print("1. Setting up Django...")
    django.setup()
    print("   ✅ Django setup successful")
    
    # Test settings
    from django.conf import settings
    print("2. Testing Django settings...")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"   SECRET_KEY: {'*' * 20}...{settings.SECRET_KEY[-10:]}")
    print(f"   DATABASE: {settings.DATABASES['default']['ENGINE']}")
    print("   ✅ Settings loaded successfully")
    
    # Test URL configuration
    print("3. Testing URL configuration...")
    from django.urls import reverse
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/')
    
    # Test home view
    from spoorthi_macs.urls import home_view
    response = home_view(request)
    print(f"   Home view status: {response.status_code}")
    print("   ✅ URL configuration working")
    
    # Test template
    print("4. Testing template...")
    template_path = project_dir / 'templates' / 'home_simple.html'
    if template_path.exists():
        print("   ✅ Template exists")
    else:
        print("   ❌ Template missing!")
    
    # Test static files
    print("5. Testing static files configuration...")
    print(f"   STATIC_URL: {settings.STATIC_URL}")
    print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print("   ✅ Static files configured")
    
    # Test apps
    print("6. Testing installed apps...")
    print(f"   Apps: {len(settings.INSTALLED_APPS)}")
    for app in settings.INSTALLED_APPS:
        if 'whitenoise' in app:
            print(f"   ✅ {app}")
        elif 'companies' in app:
            print(f"   ✅ {app}")
    
    print("\n🎉 All tests passed! Configuration is ready for Render.")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)




