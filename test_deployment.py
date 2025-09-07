#!/usr/bin/env python
"""
SML777 - Deployment Test Script
==============================

This script tests all components of the deployment configuration.
"""

import os
import sys
import django
from pathlib import Path

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        import dj_database_url
        print("✅ dj_database_url imported successfully")
    except ImportError as e:
        print(f"❌ dj_database_url import failed: {e}")
        return False
    
    try:
        import whitenoise
        print("✅ whitenoise imported successfully")
    except ImportError as e:
        print(f"❌ whitenoise import failed: {e}")
        return False
    
    try:
        import gunicorn
        print("✅ gunicorn imported successfully")
    except ImportError as e:
        print(f"❌ gunicorn import failed: {e}")
        return False
    
    return True

def test_django_setup():
    """Test Django setup with production settings"""
    print("\n🔍 Testing Django setup...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings_production')
        django.setup()
        print("✅ Django setup successful")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_apps():
    """Test that all apps are properly configured"""
    print("\n🔍 Testing app configuration...")
    
    try:
        from django.conf import settings
        
        # Check INSTALLED_APPS
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'whitenoise.runserver_nostatic',
            'companies',
        ]
        
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print(f"✅ {app} is installed")
            else:
                print(f"❌ {app} is missing")
                return False
        
        # Check context processor
        context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
        if 'companies.context_processors.user_header_info' in context_processors:
            print("✅ Context processor configured")
        else:
            print("❌ Context processor missing")
            return False
        
        return True
    except Exception as e:
        print(f"❌ App configuration test failed: {e}")
        return False

def test_database():
    """Test database configuration"""
    print("\n🔍 Testing database configuration...")
    
    try:
        from django.conf import settings
        from django.db import connection
        
        # Test database connection
        connection.ensure_connection()
        print("✅ Database connection successful")
        
        # Check database engine
        engine = settings.DATABASES['default']['ENGINE']
        print(f"✅ Database engine: {engine}")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_static_files():
    """Test static files configuration"""
    print("\n🔍 Testing static files configuration...")
    
    try:
        from django.conf import settings
        
        # Check static files settings
        if hasattr(settings, 'STATICFILES_STORAGE'):
            print(f"✅ Static files storage: {settings.STATICFILES_STORAGE}")
        else:
            print("❌ Static files storage not configured")
            return False
        
        if hasattr(settings, 'STATIC_ROOT'):
            print(f"✅ Static root: {settings.STATIC_ROOT}")
        else:
            print("❌ Static root not configured")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Static files test failed: {e}")
        return False

def test_security():
    """Test security configuration"""
    print("\n🔍 Testing security configuration...")
    
    try:
        from django.conf import settings
        
        # Check security settings
        if not settings.DEBUG:
            print("✅ DEBUG is False (production mode)")
        else:
            print("⚠️ DEBUG is True (development mode)")
        
        if hasattr(settings, 'SECRET_KEY') and settings.SECRET_KEY:
            print("✅ SECRET_KEY is configured")
        else:
            print("❌ SECRET_KEY is missing")
            return False
        
        if hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
            print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        else:
            print("❌ ALLOWED_HOSTS not configured")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Security test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SML777 Deployment Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_django_setup,
        test_apps,
        test_database,
        test_static_files,
        test_security,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your deployment is ready!")
        return 0
    else:
        print("❌ Some tests failed. Please check the configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
