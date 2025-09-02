#!/usr/bin/env python
"""
Script to debug role flags functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.views import role_flags, _flag
from companies.models import Users, UserPermission
from django.contrib.auth.models import User

def debug_role_flags():
    """Debug role flags for a specific user."""
    
    print("=== ROLE FLAGS DEBUG ===")
    
    # Get the user
    try:
        user = User.objects.get(username='jagadeesh')
        print(f"User: {user.username}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Is Superuser: {user.is_superuser}")
    except User.DoesNotExist:
        print("User 'jagadeesh' not found")
        return
    
    # Get profile
    from companies.views import get_profile_for_user
    profile = get_profile_for_user(user)
    print(f"\nProfile: {profile}")
    
    if profile:
        print(f"Profile ID: {profile.id}")
        print(f"Profile full_name: {profile.full_name}")
        
        # Check UserPermission directly
        try:
            user_perm = UserPermission.objects.filter(user_profile=profile).first()
            if user_perm:
                print(f"\nUserPermission found: ID {user_perm.id}")
                print(f"  is_admin: {user_perm.is_admin}")
                print(f"  is_master: {user_perm.is_master}")
                print(f"  is_data_entry: {user_perm.is_data_entry}")
                print(f"  is_accounting: {user_perm.is_accounting}")
                print(f"  is_recovery_agent: {user_perm.is_recovery_agent}")
                print(f"  is_auditor: {user_perm.is_auditor}")
                print(f"  is_manager: {user_perm.is_manager}")
                
                # Test _flag function
                print(f"\nTesting _flag function:")
                print(f"  _flag(is_admin): {_flag(user_perm, 'is_admin')}")
                print(f"  _flag(is_master): {_flag(user_perm, 'is_master')}")
                print(f"  _flag(is_data_entry): {_flag(user_perm, 'is_data_entry')}")
            else:
                print("No UserPermission record found")
        except Exception as e:
            print(f"Error checking UserPermission: {e}")
    
    # Get role flags
    try:
        rf = role_flags(user)
        print(f"\nRole Flags Result:")
        print(f"  admin: {rf['admin']}")
        print(f"  master: {rf['master']}")
        print(f"  data_entry: {rf['data_entry']}")
        print(f"  accounting: {rf['accounting']}")
        print(f"  recovery_agent: {rf['recovery_agent']}")
        print(f"  auditor: {rf['auditor']}")
        print(f"  manager: {rf['manager']}")
        print(f"  profile: {rf['profile']}")
        
        # Test can_user_delete_entity
        from companies.views import can_user_delete_entity
        print("\nDelete Permissions:")
        test_entities = ['company', 'branch', 'users', 'client', 'loanapplication']
        for entity in test_entities:
            can_delete = can_user_delete_entity(user, entity)
            print(f"  {entity}: {can_delete}")
            
    except Exception as e:
        print(f"Error getting role flags: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_role_flags()
