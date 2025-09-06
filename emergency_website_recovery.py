#!/usr/bin/env python
"""
EMERGENCY WEBSITE RECOVERY SCRIPT
This script helps recover the website from any JavaScript issues
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.core.cache import cache

def emergency_recovery():
    print("🚨 EMERGENCY WEBSITE RECOVERY STARTED")
    print("=" * 50)
    
    # Clear all caches
    print("1. Clearing Django cache...")
    try:
        cache.clear()
        print("   ✅ Cache cleared successfully")
    except Exception as e:
        print(f"   ❌ Cache clear failed: {e}")
    
    # Clear browser cache instructions
    print("\n2. Browser cache clearing instructions:")
    print("   - Press Ctrl+F5 to hard refresh")
    print("   - Or press Ctrl+Shift+R")
    print("   - Or clear browser cache manually")
    
    # Check if server is running
    print("\n3. Checking server status...")
    try:
        from django.test import Client
        client = Client()
        response = client.get('/')
        print(f"   ✅ Server responding: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Server issue: {e}")
    
    # Static files check
    print("\n4. Checking static files...")
    static_dir = os.path.join(os.getcwd(), 'staticfiles')
    if os.path.exists(static_dir):
        print("   ✅ Static files directory exists")
    else:
        print("   ❌ Static files directory missing")
    
    # Template check
    print("\n5. Checking templates...")
    template_dir = os.path.join(os.getcwd(), 'templates')
    if os.path.exists(template_dir):
        print("   ✅ Templates directory exists")
    else:
        print("   ❌ Templates directory missing")
    
    print("\n" + "=" * 50)
    print("🎯 RECOVERY ACTIONS COMPLETED")
    print("\nNext steps:")
    print("1. Hard refresh your browser (Ctrl+F5)")
    print("2. Clear browser cache if needed")
    print("3. Restart Django server if necessary")
    print("4. Check browser console for any remaining errors")

if __name__ == '__main__':
    emergency_recovery()


