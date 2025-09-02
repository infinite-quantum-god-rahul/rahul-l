#!/usr/bin/env python
"""
Script to restore an inactive branch to active status so it appears in the grid.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import Branch

def restore_branch():
    """Restore inactive branch to active status so it appears in the grid."""
    
    print("=== Branch Restoration Script ===")
    
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
    print("\nNext steps:")
    print("1. Go to the Branch grid in your application")
    print("2. You should now see the restored branch in the list")
    print("3. Use the delete button to permanently remove it when ready")

if __name__ == "__main__":
    try:
        restore_branch()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
