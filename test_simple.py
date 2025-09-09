#!/usr/bin/env python3
"""
Simple test to verify the deployment works
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
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-deployment')

# Mock DATABASE_URL for testing
os.environ.setdefault('DATABASE_URL', 'postgresql://user:pass@localhost:5432/testdb')

print("🔍 Testing Simple Deployment...")

try:
    django.setup()
    print("✅ Django setup successful")
    
    from django.test import RequestFactory
    from spoorthi_macs.urls import home_view
    
    factory = RequestFactory()
    request = factory.get('/')
    response = home_view(request)
    
    print(f"✅ Home view status: {response.status_code}")
    print("✅ Deployment test passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()




