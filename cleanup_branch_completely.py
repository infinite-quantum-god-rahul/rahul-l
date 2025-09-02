#!/usr/bin/env python
"""
Script to completely clean up a branch and all its related records.
This will delete Staff, Users, UserPermissions, and then the Branch itself.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import Branch, Staff, Users, UserPermission

def cleanup_branch_completely():
    """Completely clean up a branch and all related records."""
    
    print("=== COMPLETE BRANCH CLEANUP SCRIPT ===")
    
    # Find the branch to delete
    branch = Branch.objects.first()
    if not branch:
        print("No branches found in database.")
        return
    
    print(f"Branch to delete: {branch.code} - {branch.name} (ID: {branch.id})")
    
    # Show all related records before deletion
    print("\n=== RELATED RECORDS TO BE DELETED ===")
    
    # Staff records
    staff_records = Staff.objects.filter(branch=branch)
    print(f"Staff records: {staff_records.count()}")
    for staff in staff_records:
        print(f"  - {staff.staffcode}: {staff.name}")
    
    # Users records
    users_records = Users.objects.filter(branch=branch)
    print(f"Users records: {users_records.count()}")
    for user in users_records:
        print(f"  - {user.full_name}")
    
    # UserPermission records
    up_records = UserPermission.objects.filter(user_profile__branch=branch)
    print(f"UserPermission records: {up_records.count()}")
    for up in up_records:
        print(f"  - User: {up.user_profile.full_name}")
    
    # Confirm deletion
    print(f"\n⚠️  WARNING: This will permanently delete:")
    print(f"   - {staff_records.count()} Staff records")
    print(f"   - {users_records.count()} Users records")
    print(f"   - {up_records.count()} UserPermission records")
    print(f"   - The Branch '{branch.name}' itself")
    
    response = input("\nAre you sure you want to proceed? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Operation cancelled.")
        return
    
    print(f"\n=== STARTING CLEANUP ===")
    
    try:
        # Delete UserPermissions first (they reference Users)
        print("1. Deleting UserPermission records...")
        up_count = up_records.count()
        up_records.delete()
        print(f"   ✓ Deleted {up_count} UserPermission records")
        
        # Delete Users records
        print("2. Deleting Users records...")
        users_count = users_records.count()
        users_records.delete()
        print(f"   ✓ Deleted {users_count} Users records")
        
        # Delete Staff records
        print("3. Deleting Staff records...")
        staff_count = staff_records.count()
        staff_records.delete()
        print(f"   ✓ Deleted {staff_count} Staff records")
        
        # Finally delete the Branch
        print("4. Deleting Branch...")
        branch_name = branch.name
        branch_code = branch.code
        branch.delete()
        print(f"   ✓ Deleted Branch: {branch_code} - {branch_name}")
        
        print(f"\n=== CLEANUP COMPLETE ===")
        print(f"✓ All related records and the branch have been permanently deleted.")
        
        # Verify cleanup
        print(f"\n=== VERIFICATION ===")
        print(f"Remaining branches: {Branch.objects.count()}")
        print(f"Remaining staff: {Staff.objects.count()}")
        print(f"Remaining users: {Users.objects.count()}")
        print(f"Remaining user permissions: {UserPermission.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    try:
        cleanup_branch_completely()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
