#!/usr/bin/env python
"""
Fix corrupted user_id data in companies_users table
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import Users
from django.contrib.auth.models import User

def fix_users_data():
    print("=== Fixing corrupted Users data ===")
    
    # Find corrupted records
    corrupted_users = Users.objects.filter(user_id__isnull=False).exclude(user_id__regex=r'^\d+$')
    print(f"Found {corrupted_users.count()} corrupted user records")
    
    if corrupted_users.count() == 0:
        print("No corrupted data found!")
        return
    
    # Show corrupted records
    print("\nCorrupted records:")
    for user in corrupted_users:
        print(f"  ID: {user.id}, user_id: '{user.user_id}', user: {user.user}")
    
    # Fix corrupted records by setting user_id to None
    print("\nFixing corrupted records...")
    fixed_count = 0
    
    for user in corrupted_users:
        try:
            old_user_id = user.user_id
            user.user_id = None
            user.save()
            print(f"  Fixed user {user.id}: cleared user_id '{old_user_id}'")
            fixed_count += 1
        except Exception as e:
            print(f"  Error fixing user {user.id}: {e}")
    
    print(f"\nFixed {fixed_count} corrupted user records")
    
    # Verify fix
    remaining_corrupted = Users.objects.filter(user_id__isnull=False).exclude(user_id__regex=r'^\d+$')
    print(f"Remaining corrupted records: {remaining_corrupted.count()}")
    
    if remaining_corrupted.count() == 0:
        print("✅ All corrupted data fixed successfully!")
    else:
        print("❌ Some corrupted data remains")

if __name__ == "__main__":
    fix_users_data()
