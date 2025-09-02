#!/usr/bin/env python
"""
Script to restore a branch for manual testing of deletion functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import Branch, Company

def restore_branch_for_testing():
    """Restore a branch for manual testing."""
    
    print("=== RESTORE BRANCH FOR TESTING ===")
    
    # Check if we have a company
    company = Company.objects.first()
    if not company:
        print("No company found. Creating a default company...")
        company = Company.objects.create(
            code="CMP001",
            name="Test Company",
            status="active"
        )
        print(f"✓ Created company: {company.code} - {company.name}")
    
    # Check existing branches
    existing_branches = Branch.objects.all()
    print(f"\nExisting branches: {existing_branches.count()}")
    for branch in existing_branches:
        print(f"  - {branch.code}: {branch.name} (Status: {branch.status})")
    
    # Create a test branch if none exists
    if existing_branches.count() == 0:
        print("\nNo branches found. Creating a test branch...")
        test_branch = Branch.objects.create(
            code="BRN001",
            name="Test Branch",
            company=company,
            status="active"
        )
        print(f"✓ Created test branch: {test_branch.code} - {test_branch.name}")
    else:
        print("\n✓ Branch already exists and is ready for testing")
    
    # Show final state
    print(f"\n=== FINAL STATE ===")
    all_branches = Branch.objects.all()
    for branch in all_branches:
        print(f"  - {branch.code}: {branch.name} (Status: {branch.status})")
    
    print(f"\nNow you can:")
    print(f"1. Go to the Branch grid in your web application")
    print(f"2. See the branch in the list")
    print(f"3. Test the delete functionality manually")
    print(f"4. Observe what happens when you delete it")

if __name__ == "__main__":
    try:
        restore_branch_for_testing()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
