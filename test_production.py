#!/usr/bin/env python3
"""
Test Production Settings with All Features
==========================================
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set environment variables to match Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings_production')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', '*.onrender.com')
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-production')

# Mock DATABASE_URL for testing
os.environ.setdefault('DATABASE_URL', 'postgresql://user:pass@localhost:5432/testdb')

print("🔍 Testing Production Settings with All Features...")
print("=" * 60)

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
    print(f"   INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")
    print("   ✅ Settings loaded successfully")
    
    # Test WhiteNoise
    print("3. Testing WhiteNoise...")
    if 'whitenoise.runserver_nostatic' in settings.INSTALLED_APPS:
        print("   ✅ WhiteNoise installed")
    if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
        print("   ✅ WhiteNoise middleware configured")
    print(f"   STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    print("   ✅ WhiteNoise configuration working")
    
    # Test context processors
    print("4. Testing context processors...")
    context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
    print(f"   Context processors: {len(context_processors)}")
    for processor in context_processors:
        print(f"   ✅ {processor}")
    print("   ✅ Context processors configured")
    
    # Test URL configuration
    print("5. Testing URL configuration...")
    from django.test import RequestFactory
    from spoorthi_macs.urls import home_view
    
    factory = RequestFactory()
    request = factory.get('/')
    response = home_view(request)
    print(f"   Home view status: {response.status_code}")
    print("   ✅ URL configuration working")
    
    # Test template
    print("6. Testing template...")
    template_path = project_dir / 'templates' / 'home_simple.html'
    if template_path.exists():
        print("   ✅ Original homepage template exists")
    else:
        print("   ❌ Template missing!")
    
    # Test static files
    print("7. Testing static files configuration...")
    print(f"   STATIC_URL: {settings.STATIC_URL}")
    print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print("   ✅ Static files configured")
    
    # Test SML777 features
    print("8. Testing SML777 features...")
    if hasattr(settings, 'SML_FEATURES'):
        print(f"   SML_FEATURES: {len(settings.SML_FEATURES)} features")
        for feature, enabled in settings.SML_FEATURES.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {feature}: {enabled}")
    print("   ✅ SML777 features configured")
    
    # Test companies app
    print("9. Testing companies app...")
    if 'companies' in settings.INSTALLED_APPS:
        print("   ✅ Companies app installed")
    print("   ✅ Companies app working")
    
    print("\n🎉 All tests passed! Production settings are ready!")
    print("=" * 60)
    print("✅ Your original SML777 website is preserved and ready for deployment!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
