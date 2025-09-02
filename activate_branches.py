#!/usr/bin/env python
"""
Script to activate branches so they appear in the grid for manual testing.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import Branch

def activate_branches():
    """Activate all branches so they appear in the grid."""
    
    print("=== ACTIVATE BRANCHES FOR TESTING ===")
    
    # Get all branches
    branches = Branch.objects.all()
    print(f"Found {branches.count()} branches:")
    
    for branch in branches:
        print(f"  - {branch.code}: {branch.name} (Current Status: {branch.status})")
    
    # Activate all branches
    print(f"\nActivating all branches...")
    for branch in branches:
        if branch.status != 'active':
            branch.status = 'active'
            branch.save()
            print(f"  ✓ Activated {branch.code}: {branch.name}")
        else:
            print(f"  - {branch.code}: {branch.name} is already active")
    
    # Show final state
    print(f"\n=== FINAL STATE ===")
    all_branches = Branch.objects.all()
    for branch in all_branches:
        print(f"  - {branch.code}: {branch.name} (Status: {branch.status})")
    
    print(f"\n✓ All branches are now ACTIVE and will appear in your grid!")
    print(f"\nNow you can:")
    print(f"1. Go to the Branch grid in your web application")
    print(f"2. See both branches in the list")
    print(f"3. Test the delete functionality manually on either branch")
    print(f"4. Observe what happens when you delete it")

if __name__ == "__main__":
    try:
        activate_branches()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
