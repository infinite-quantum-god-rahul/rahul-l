#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.urls import reverse, resolve
from django.test import Client
from companies.models import UserProfile
from django.contrib.auth.models import User

def test_userprofile():
    print("🔍 TESTING USERPROFILE FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Check if UserProfile model exists
    print("1. Testing UserProfile model...")
    try:
        profile_count = UserProfile.objects.count()
        print(f"   ✅ UserProfile model works: {profile_count} profiles found")
    except Exception as e:
        print(f"   ❌ UserProfile model error: {e}")
        return
    
    # Test 2: Check URL resolution
    print("\n2. Testing URL resolution...")
    try:
        list_url = reverse('userprofile_list')
        create_url = reverse('userprofile_create')
        print(f"   ✅ userprofile_list: {list_url}")
        print(f"   ✅ userprofile_create: {create_url}")
    except Exception as e:
        print(f"   ❌ URL resolution error: {e}")
        return
    
    # Test 3: Test URL patterns
    print("\n3. Testing URL patterns...")
    try:
        resolver = resolve('/userprofile/')
        print(f"   ✅ /userprofile/ resolves to: {resolver.view_name}")
        print(f"   ✅ View function: {resolver.func.__name__}")
    except Exception as e:
        print(f"   ❌ URL pattern error: {e}")
    
    # Test 4: Test with client
    print("\n4. Testing with Django client...")
    client = Client()
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("   ✅ Created test user")
    
    # Login
    login_success = client.login(username='testuser', password='testpass123')
    print(f"   ✅ Login successful: {login_success}")
    
    # Test UserProfile list
    try:
        response = client.get('/userprofile/')
        print(f"   ✅ UserProfile list response: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ UserProfile list page loads successfully!")
        else:
            print(f"   ❌ UserProfile list failed with status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ UserProfile list error: {e}")
    
    # Test UserProfile create form (GET)
    try:
        response = client.get('/userprofile/get/')
        print(f"   ✅ UserProfile get form response: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ UserProfile get form page loads successfully!")
        else:
            print(f"   ❌ UserProfile get form failed with status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ UserProfile get form error: {e}")
    
    # Test UserProfile create (POST)
    try:
        response = client.post('/userprofile/create/', {})
        print(f"   ✅ UserProfile create POST response: {response.status_code}")
        if response.status_code in [200, 400]:  # 400 is expected for empty form
            print("   ✅ UserProfile create POST works!")
        else:
            print(f"   ❌ UserProfile create POST failed with status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ UserProfile create POST error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 DEBUG COMPLETE")

if __name__ == '__main__':
    test_userprofile()
