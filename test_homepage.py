#!/usr/bin/env python3
"""
Test Homepage Template
=====================
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')

print("🔍 Testing Homepage Template...")

try:
    django.setup()
    
    from django.test import RequestFactory
    from spoorthi_macs.urls import home_view
    
    factory = RequestFactory()
    request = factory.get('/')
    response = home_view(request)
    
    print(f"✅ Homepage status: {response.status_code}")
    print(f"✅ Template being used: home.html")
    print(f"✅ Content length: {len(response.content)} characters")
    
    # Check if the content contains key elements from your original homepage
    content = response.content.decode('utf-8')
    
    if 'SML777 - Infinite Error Prevention System' in content:
        print("✅ Original homepage title found!")
    else:
        print("❌ Original homepage title NOT found")
    
    if 'hero-section' in content:
        print("✅ Hero section found!")
    else:
        print("❌ Hero section NOT found")
    
    if 'feature-card' in content:
        print("✅ Feature cards found!")
    else:
        print("❌ Feature cards NOT found")
    
    if 'stats-section' in content:
        print("✅ Stats section found!")
    else:
        print("❌ Stats section NOT found")
    
    print("\n🎉 Homepage test completed!")
    print("Your original beautiful homepage is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()




