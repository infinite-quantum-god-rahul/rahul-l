#!/usr/bin/env python
"""
Debug script for Render deployment issues
"""
import os
import sys

def check_environment():
    """Check environment variables"""
    print("🔍 Environment Variables:")
    print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE', 'Not set')}")
    print(f"DEBUG: {os.getenv('DEBUG', 'Not set')}")
    print(f"DATABASE_URL: {'Set' if os.getenv('DATABASE_URL') else 'Not set'}")
    print(f"SECRET_KEY: {'Set' if os.getenv('SECRET_KEY') else 'Not set'}")
    print()

def check_imports():
    """Check critical imports"""
    print("🔍 Checking imports:")
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        return False
    
    try:
        import dj_database_url
        print("✅ dj_database_url")
    except ImportError as e:
        print(f"❌ dj_database_url import failed: {e}")
        return False
    
    try:
        import whitenoise
        print("✅ whitenoise")
    except ImportError as e:
        print(f"❌ whitenoise import failed: {e}")
        return False
    
    return True

def check_django_setup():
    """Check Django setup"""
    print("🔍 Django setup:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
        import django
        django.setup()
        print("✅ Django setup successful")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def check_database():
    """Check database connection"""
    print("🔍 Database connection:")
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_apps():
    """Check app configuration"""
    print("🔍 App configuration:")
    try:
        from django.conf import settings
        
        # Check companies app
        if 'companies' in settings.INSTALLED_APPS:
            print("✅ companies app is installed")
        else:
            print("❌ companies app is missing")
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
        print(f"❌ App configuration check failed: {e}")
        return False

def main():
    """Run all checks"""
    print("🚀 Render Deployment Debug")
    print("=" * 40)
    
    check_environment()
    
    if not check_imports():
        print("❌ Import check failed")
        return 1
    
    if not check_django_setup():
        print("❌ Django setup failed")
        return 1
    
    if not check_database():
        print("❌ Database check failed")
        return 1
    
    if not check_apps():
        print("❌ App configuration check failed")
        return 1
    
    print("✅ All checks passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())




