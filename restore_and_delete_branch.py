#!/usr/bin/env python
"""
Script to restore an inactive branch to active status and then permanently delete it.
This allows you to see the branch in the grid before permanently removing it.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import Branch

def restore_and_delete_branch():
    """Restore inactive branch to active, then delete it permanently."""
    
    print("=== Branch Management Script ===")
    
    # Find all branches
    all_branches = Branch.objects.all()
    print(f"Total branches in database: {all_branches.count()}")
    
    # Show all branches with their status
    print("\nAll branches:")
    for branch in all_branches:
        print(f"  ID: {branch.id}, Code: {branch.code}, Name: {branch.name}, Status: {branch.status}")
    
    # Find inactive branches
    inactive_branches = Branch.objects.filter(status='inactive')
    print(f"\nInactive branches: {inactive_branches.count()}")
    
    if not inactive_branches.exists():
        print("No inactive branches found. Nothing to restore.")
        return
    
    # Restore first inactive branch to active
    branch_to_restore = inactive_branches.first()
    print(f"\nRestoring branch '{branch_to_restore.name}' (ID: {branch_to_restore.id}) to active status...")
    
    branch_to_restore.status = 'active'
    branch_to_restore.save()
    
    print(f"✓ Branch '{branch_to_restore.name}' is now ACTIVE and will appear in the grid.")
    print("\nNow you can:")
    print("1. Go to the Branch grid in your application")
    print("2. See the restored branch in the list")
    print("3. Use the delete button to permanently remove it")
    
    # Ask if user wants to delete it now
    response = input("\nDo you want to delete this branch permanently now? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        print(f"\nDeleting branch '{branch_to_restore.name}' permanently...")
        branch_name = branch_to_restore.name
        branch_to_restore.delete()
        print(f"✓ Branch '{branch_name}' has been permanently deleted from the database.")
        
        # Verify deletion
        remaining_branches = Branch.objects.all()
        print(f"\nRemaining branches: {remaining_branches.count()}")
        for branch in remaining_branches:
            print(f"  ID: {branch.id}, Code: {branch.code}, Name: {branch.name}, Status: {branch.status}")
    else:
        print(f"\nBranch '{branch_to_restore.name}' is now active and visible in the grid.")
        print("You can delete it manually through the web interface when ready.")

if __name__ == "__main__":
    try:
        restore_and_delete_branch()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
