#!/usr/bin/env python
"""
Script to test cascade deletion of a branch and all its related records.
This will delete the branch and all related Staff, Users, and UserPermissions.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import Branch, Staff, Users, UserPermission

def test_cascade_deletion():
    """Test cascade deletion of a branch and all related records."""
    
    print("=== TEST CASCADE DELETION ===")
    
    # Show current state
    branches = Branch.objects.all()
    print(f"Current branches: {branches.count()}")
    for branch in branches:
        print(f"  - {branch.code}: {branch.name}")
    
    if branches.count() == 0:
        print("No branches to delete.")
        return
    
    # Let user choose which branch to delete
    print(f"\nWhich branch do you want to delete?")
    for i, branch in enumerate(branches):
        print(f"  {i+1}. {branch.code}: {branch.name}")
    
    try:
        choice = int(input(f"\nEnter choice (1-{branches.count()}): ")) - 1
        if choice < 0 or choice >= branches.count():
            print("Invalid choice.")
            return
        branch_to_delete = branches[choice]
    except ValueError:
        print("Invalid input.")
        return
    
    print(f"\n=== BRANCH TO DELETE ===")
    print(f"Branch: {branch_to_delete.code} - {branch_to_delete.name}")
    
    # Count related records
    staff_records = Staff.objects.filter(branch=branch_to_delete)
    users_records = Users.objects.filter(branch=branch_to_delete)
    up_records = UserPermission.objects.filter(user_profile__branch=branch_to_delete)
    
    print(f"\nRelated records to be deleted:")
    print(f"  - Staff: {staff_records.count()}")
    for staff in staff_records:
        print(f"    * {staff.staffcode}: {staff.name}")
    
    print(f"  - Users: {users_records.count()}")
    for user in users_records:
        print(f"    * {user.full_name}")
    
    print(f"  - UserPermissions: {up_records.count()}")
    for up in up_records:
        print(f"    * User: {up.user_profile.full_name}")
    
    # Confirm deletion
    confirm = input(f"\n⚠️  Are you sure you want to delete branch '{branch_to_delete.name}' and ALL related records? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    print(f"\n=== STARTING CASCADE DELETION ===")
    
    try:
        # Delete UserPermissions first (they reference Users)
        if up_records.count() > 0:
            print("1. Deleting UserPermission records...")
            up_count = up_records.count()
            up_records.delete()
            print(f"   ✓ Deleted {up_count} UserPermission records")
        
        # Delete Users records
        if users_records.count() > 0:
            print("2. Deleting Users records...")
            users_count = users_records.count()
            users_records.delete()
            print(f"   ✓ Deleted {users_count} Users records")
        
        # Delete Staff records
        if staff_records.count() > 0:
            print("3. Deleting Staff records...")
            staff_count = staff_records.count()
            staff_records.delete()
            print(f"   ✓ Deleted {staff_count} Staff records")
        
        # Finally delete the Branch
        print("4. Deleting Branch...")
        branch_name = branch_to_delete.name
        branch_code = branch_to_delete.code
        branch_to_delete.delete()
        print(f"   ✓ Deleted Branch: {branch_code} - {branch_name}")
        
        print(f"\n=== CASCADE DELETION COMPLETE ===")
        print(f"✓ Branch '{branch_name}' and all related records have been permanently deleted.")
        
        # Verify cleanup
        print(f"\n=== VERIFICATION ===")
        remaining_branches = Branch.objects.all()
        print(f"Remaining branches: {remaining_branches.count()}")
        if remaining_branches.count() > 0:
            print("Remaining branches:")
            for branch in remaining_branches:
                print(f"  - {branch.code}: {branch.name}")
        
        print(f"Remaining staff: {Staff.objects.count()}")
        print(f"Remaining users: {Users.objects.count()}")
        print(f"Remaining user permissions: {UserPermission.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error during deletion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        test_cascade_deletion()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
