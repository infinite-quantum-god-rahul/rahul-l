#!/usr/bin/env python3
"""
SML777 Deployment Test Script
============================

Test the ultra-minimal Django configuration locally.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings_ultra_minimal')

def test_django_setup():
    """Test if Django can be set up with ultra-minimal settings"""
    try:
        django.setup()
        print("✅ Django setup successful!")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✅ Database connection successful!")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_urls():
    """Test URL configuration"""
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test home view
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home view working!")
        else:
            print(f"❌ Home view failed: {response.status_code}")
            return False
            
        # Test health view
        response = client.get('/health/')
        if response.status_code == 200:
            print("✅ Health view working!")
        else:
            print(f"❌ Health view failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ URL testing failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing SML777 Ultra-Minimal Configuration")
    print("=" * 50)
    
    tests = [
        ("Django Setup", test_django_setup),
        ("Database Connection", test_database),
        ("URL Configuration", test_urls),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment!")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)