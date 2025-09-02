#!/usr/bin/env python
"""
Script to create a test branch for testing deletion functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import Branch, Company

def create_test_branch():
    """Create a test branch for testing deletion."""
    
    print("=== CREATE TEST BRANCH SCRIPT ===")
    
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
    
    # Create a test branch
    test_branch = Branch.objects.create(
        code="BRN002",
        name="Test Branch",
        company=company,
        status="active"
    )
    
    print(f"\n✓ Created test branch: {test_branch.code} - {test_branch.name}")
    print(f"  Company: {test_branch.company.name}")
    print(f"  Status: {test_branch.status}")
    
    # Show all branches now
    print(f"\n=== ALL BRANCHES AFTER CREATION ===")
    all_branches = Branch.objects.all()
    for branch in all_branches:
        print(f"  - {branch.code}: {branch.name} (Status: {branch.status})")
    
    print(f"\nNow you can:")
    print(f"1. Go to the Branch grid in your application")
    print(f"2. See the new test branch 'BRN002' in the list")
    print(f"3. Test the delete functionality manually")

if __name__ == "__main__":
    try:
        create_test_branch()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
