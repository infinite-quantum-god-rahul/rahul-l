#!/usr/bin/env python
"""
Safe Branch Deletion Script
This script safely deletes a branch and ALL its related records to prevent
FOREIGN KEY constraint errors. It handles the deletion in the correct order
to avoid database constraint violations.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.models import (
    Branch, Staff, Users, UserPermission, Village, Center, Group, 
    Client, LoanApplication, LoanApproval, Disbursement, Prepaid, 
    Mortgage, ExSaving, Cadre
)

def get_all_related_records(branch):
    """Get all records that reference this branch."""
    print(f"Scanning for records related to branch: {branch.code} - {branch.name}")
    
    related_data = {}
    
    # Direct relationships
    related_data['cadre'] = Cadre.objects.filter(branch=branch)
    related_data['staff'] = Staff.objects.filter(branch=branch)
    related_data['users'] = Users.objects.filter(branch=branch)
    related_data['villages'] = Village.objects.filter(branch=branch)
    
    # Indirect relationships through villages
    if related_data['villages'].exists():
        related_data['centers'] = Center.objects.filter(village__branch=branch)
        
        if related_data['centers'].exists():
            related_data['groups'] = Group.objects.filter(center__village__branch=branch)
            
            if related_data['groups'].exists():
                related_data['clients'] = Client.objects.filter(group__center__village__branch=branch)
                
                if related_data['clients'].exists():
                    client_codes = related_data['clients'].values_list('smtcode', flat=True)
                    related_data['loan_applications'] = LoanApplication.objects.filter(
                        client__group__center__village__branch=branch
                    )
                    related_data['loan_approvals'] = LoanApproval.objects.filter(
                        loan_application__client__group__center__village__branch=branch
                    )
                    related_data['disbursements'] = Disbursement.objects.filter(
                        loan_application__client__group__center__village__branch=branch
                    )
                    related_data['prepaid'] = Prepaid.objects.filter(member_code__in=client_codes)
                    related_data['mortgage'] = Mortgage.objects.filter(member_code__in=client_codes)
                    related_data['ex_savings'] = ExSaving.objects.filter(member_code__in=client_codes)
                else:
                    related_data['clients'] = Client.objects.none()
                    related_data['loan_applications'] = LoanApplication.objects.none()
                    related_data['loan_approvals'] = LoanApproval.objects.none()
                    related_data['disbursements'] = Disbursement.objects.none()
                    related_data['prepaid'] = Prepaid.objects.none()
                    related_data['mortgage'] = Mortgage.objects.none()
                    related_data['ex_savings'] = ExSaving.objects.none()
            else:
                related_data['groups'] = Group.objects.none()
                related_data['clients'] = Client.objects.none()
                related_data['loan_applications'] = LoanApplication.objects.none()
                related_data['loan_approvals'] = LoanApproval.objects.none()
                related_data['disbursements'] = Disbursement.objects.none()
                related_data['prepaid'] = Prepaid.objects.none()
                related_data['mortgage'] = Mortgage.objects.none()
                related_data['ex_savings'] = ExSaving.objects.none()
        else:
            related_data['centers'] = Center.objects.none()
            related_data['groups'] = Group.objects.none()
            related_data['clients'] = Client.objects.none()
            related_data['loan_applications'] = LoanApplication.objects.none()
            related_data['loan_approvals'] = LoanApproval.objects.none()
            related_data['disbursements'] = Disbursement.objects.none()
            related_data['prepaid'] = Prepaid.objects.none()
            related_data['mortgage'] = Mortgage.objects.none()
            related_data['ex_savings'] = ExSaving.objects.none()
    else:
        related_data['centers'] = Center.objects.none()
        related_data['groups'] = Group.objects.none()
        related_data['clients'] = Client.objects.none()
        related_data['loan_applications'] = LoanApplication.objects.none()
        related_data['loan_approvals'] = LoanApproval.objects.none()
        related_data['disbursements'] = Disbursement.objects.none()
        related_data['prepaid'] = Prepaid.objects.none()
        related_data['mortgage'] = Mortgage.objects.none()
        related_data['ex_savings'] = ExSaving.objects.none()
    
    return related_data

def display_deletion_summary(related_data):
    """Display what will be deleted."""
    print(f"\n{'='*60}")
    print("RECORDS TO BE DELETED")
    print(f"{'='*60}")
    
    total_records = 0
    for model_name, queryset in related_data.items():
        count = queryset.count()
        total_records += count
        print(f"  {model_name.replace('_', ' ').title():<25}: {count:>5}")
    
    print(f"{'='*60}")
    print(f"Total records to be deleted: {total_records}")
    print(f"{'='*60}")
    
    if total_records == 0:
        print("✅ No related records found. Branch can be deleted safely.")
    else:
        print("⚠️  WARNING: This will permanently delete all the above records!")
    
    return total_records

def delete_all_related_records(related_data, branch):
    """Delete all related records in the correct order to avoid FK constraint errors."""
    print(f"\n{'='*60}")
    print("STARTING CASCADE DELETION")
    print(f"{'='*60}")
    
    # Delete in reverse dependency order (most dependent first)
    deletion_order = [
        ('loan_approvals', 'Loan Approvals'),
        ('disbursements', 'Disbursements'),
        ('loan_applications', 'Loan Applications'),
        ('prepaid', 'Prepaid Records'),
        ('mortgage', 'Mortgage Records'),
        ('ex_savings', 'Ex-Savings Records'),
        ('clients', 'Clients'),
        ('groups', 'Groups'),
        ('centers', 'Centers'),
        ('villages', 'Villages'),
        ('users', 'Users'),
        ('staff', 'Staff'),
        ('cadre', 'Cadre'),
    ]
    
    for field_name, display_name in deletion_order:
        if field_name in related_data:
            queryset = related_data[field_name]
            count = queryset.count()
            if count > 0:
                print(f"🗑️  Deleting {display_name}...")
                try:
                    queryset.delete()
                    print(f"   ✅ Deleted {count} {display_name}")
                except Exception as e:
                    print(f"   ❌ Error deleting {display_name}: {e}")
                    return False
    
    # Finally delete the Branch
    print(f"🗑️  Deleting Branch...")
    try:
        branch_name = branch.name
        branch_code = branch.code
        branch.delete()
        print(f"   ✅ Deleted Branch: {branch_code} - {branch_name}")
        return True
    except Exception as e:
        print(f"   ❌ Error deleting Branch: {e}")
        return False

def verify_cleanup():
    """Verify that all records were properly cleaned up."""
    print(f"\n{'='*60}")
    print("VERIFICATION")
    print(f"{'='*60}")
    
    # Check remaining counts
    remaining_counts = {
        'Branches': Branch.objects.count(),
        'Staff': Staff.objects.count(),
        'Users': Users.objects.count(),
        'Villages': Village.objects.count(),
        'Centers': Center.objects.count(),
        'Groups': Group.objects.count(),
        'Clients': Client.objects.count(),
        'Loan Applications': LoanApplication.objects.count(),
    }
    
    for model_name, count in remaining_counts.items():
        print(f"Remaining {model_name:<20}: {count:>5}")
    
    # Check for any orphaned records
    orphaned_staff = Staff.objects.filter(branch__isnull=True).count()
    orphaned_users = Users.objects.filter(branch__isnull=True).count()
    
    if orphaned_staff > 0 or orphaned_users > 0:
        print(f"\n⚠️  Warning: {orphaned_staff} staff and {orphaned_users} users have no branch assigned")
    else:
        print(f"\n✅ All records properly cleaned up")

def main():
    """Main function to handle branch deletion."""
    print("🔧 SAFE BRANCH DELETION SCRIPT")
    print("This script will safely delete a branch and ALL related records")
    print("to prevent FOREIGN KEY constraint errors.\n")
    
    # Get branch code from user
    if len(sys.argv) > 1:
        branch_code = sys.argv[1]
    else:
        branch_code = input("Enter branch code to delete (e.g., BRN001): ").strip()
    
    if not branch_code:
        print("❌ No branch code provided. Exiting.")
        return
    
    try:
        # Find the branch
        branch = Branch.objects.get(code=branch_code)
        print(f"✅ Found branch: {branch.code} - {branch.name}")
        
        # Get all related records
        related_data = get_all_related_records(branch)
        
        # Display summary
        total_records = display_deletion_summary(related_data)
        
        if total_records == 0:
            # No related records, safe to delete
            confirm = input(f"\nDelete branch '{branch.name}'? (yes/no): ").strip().lower()
        else:
            # Has related records, need confirmation
            confirm = input(f"\nAre you sure you want to delete branch '{branch.name}' and ALL {total_records} related records? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("❌ Operation cancelled.")
            return
        
        # Perform deletion
        success = delete_all_related_records(related_data, branch)
        
        if success:
            print(f"\n{'='*60}")
            print("BRANCH DELETION COMPLETE")
            print(f"{'='*60}")
            print(f"✅ Branch '{branch.name}' and all related records have been permanently deleted.")
            
            # Verify cleanup
            verify_cleanup()
        else:
            print(f"\n❌ Branch deletion failed. Please check the errors above.")
            
    except Branch.DoesNotExist:
        print(f"❌ Branch with code '{branch_code}' not found.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
