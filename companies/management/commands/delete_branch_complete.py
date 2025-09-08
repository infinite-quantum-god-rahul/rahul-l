from django.core.management.base import BaseCommand
from django.db import connection
from companies.models import (
    Branch, Staff, Users, UserPermission, Village, Center, Group, 
    Client, LoanApplication, LoanApproval, Disbursement, Prepaid, 
    Mortgage, ExSaving, Cadre
)

class Command(BaseCommand):
    help = "Delete a branch and ALL its related records to prevent FOREIGN KEY constraint errors"

    def add_arguments(self, parser):
        parser.add_argument('branch_code', type=str, help='Branch code to delete (e.g., BRN001)')
        parser.add_argument('--force', action='store_true', help='Skip confirmation prompt')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without actually deleting')

    def handle(self, *args, **options):
        branch_code = options['branch_code']
        force = options['force']
        dry_run = options['dry_run']
        
        try:
            # Find the branch
            branch = Branch.objects.get(code=branch_code)
            
            self.stdout.write(f"Found branch: {branch.code} - {branch.name}")
            
            if dry_run:
                self.stdout.write(self.style.WARNING("DRY RUN MODE - No records will be deleted"))
            
            # Get all related records
            related_data = self._get_all_related_records(branch)
            
            # Display summary
            self._display_deletion_summary(related_data)
            
            if not force and not dry_run:
                confirm = input(f"\nAre you sure you want to delete branch '{branch.name}' and ALL related records? (yes/no): ")
                if confirm.lower() != 'yes':
                    self.stdout.write("Operation cancelled.")
                    return
            
            if dry_run:
                self.stdout.write("Dry run completed. No records were deleted.")
                return
            
            # Perform deletion
            self._delete_all_related_records(related_data, branch)
            
            self.stdout.write(f"\n=== BRANCH DELETION COMPLETE ===")
            self.stdout.write(f"✓ Branch '{branch.name}' and all related records have been permanently deleted.")
            
            # Verify cleanup
            self._verify_cleanup()
            
        except Branch.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Branch with code '{branch_code}' not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            import traceback
            traceback.print_exc()

    def _get_all_related_records(self, branch):
        """Get all records that reference this branch."""
        related_data = {}
        
        # Core models (from original script)
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
        
        # Additional CSV models with branch relationships
        try:
            # Import additional models dynamically to avoid import errors
            from companies.models import (
                MembersCsvModel, AccCashbook, AccCashbookold, Arrear, 
                MassPostingCsvModel, MasterBranchCsvModel, LoanColsCsvModel, 
                LoansCsvModel, MembersKaikaluruCsvModel, SavingsCsvModel
            )
            
            # MembersCsvModel
            related_data['members_csv'] = MembersCsvModel.objects.filter(branch=branch)
            
            # AccCashbook models
            related_data['acc_cashbook'] = AccCashbook.objects.filter(branch=branch)
            related_data['acc_cashbook_old'] = AccCashbookold.objects.filter(branch=branch)
            
            # Arrear
            related_data['arrear'] = Arrear.objects.filter(branch=branch)
            
            # MassPostingCsvModel
            related_data['mass_posting_csv'] = MassPostingCsvModel.objects.filter(branch=branch)
            
            # MasterBranchCsvModel
            related_data['master_branch_csv'] = MasterBranchCsvModel.objects.filter(branch=branch)
            
            # LoanColsCsvModel
            related_data['loan_cols_csv'] = LoanColsCsvModel.objects.filter(branch=branch)
            
            # LoansCsvModel
            related_data['loans_csv'] = LoansCsvModel.objects.filter(branch=branch)
            
            # MembersKaikaluruCsvModel
            related_data['members_kaikaluru_csv'] = MembersKaikaluruCsvModel.objects.filter(branch=branch)
            
            # SavingsCsvModel
            related_data['savings_csv'] = SavingsCsvModel.objects.filter(branch=branch)
            
        except ImportError as e:
            self.stdout.write(self.style.WARNING(f"Some models could not be imported: {e}"))
            # Create empty querysets for models that couldn't be imported
            related_data.update({
                'members_csv': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'acc_cashbook': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'acc_cashbook_old': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'arrear': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'mass_posting_csv': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'master_branch_csv': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'loan_cols_csv': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'loans_csv': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'members_kaikaluru_csv': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
                'savings_csv': type('EmptyQuerySet', (), {'count': lambda: 0, 'delete': lambda: None})(),
            })
        
        return related_data

    def _display_deletion_summary(self, related_data):
        """Display what will be deleted."""
        self.stdout.write(f"\n=== RECORDS TO BE DELETED ===")
        
        total_records = 0
        for model_name, queryset in related_data.items():
            count = queryset.count()
            total_records += count
            self.stdout.write(f"  - {model_name.replace('_', ' ').title()}: {count}")
        
        self.stdout.write(f"\nTotal records to be deleted: {total_records}")
        
        if total_records == 0:
            self.stdout.write(self.style.SUCCESS("No related records found. Branch can be deleted safely."))

    def _delete_all_related_records(self, related_data, branch):
        """Delete all related records in the correct order to avoid FK constraint errors."""
        self.stdout.write(f"\n=== STARTING CASCADE DELETION ===")
        
        # Delete in reverse dependency order (most dependent first)
        deletion_order = [
            # Core loan-related records
            ('loan_approvals', 'Loan Approvals'),
            ('disbursements', 'Disbursements'),
            ('loan_applications', 'Loan Applications'),
            ('prepaid', 'Prepaid Records'),
            ('mortgage', 'Mortgage Records'),
            ('ex_savings', 'Ex-Savings Records'),
            
            # CSV model records
            ('arrear', 'Arrear Records'),
            ('loan_cols_csv', 'Loan Columns CSV'),
            ('loans_csv', 'Loans CSV'),
            ('savings_csv', 'Savings CSV'),
            ('members_kaikaluru_csv', 'Members Kaikaluru CSV'),
            ('mass_posting_csv', 'Mass Posting CSV'),
            ('acc_cashbook', 'Account Cashbook'),
            ('acc_cashbook_old', 'Account Cashbook Old'),
            ('members_csv', 'Members CSV'),
            ('master_branch_csv', 'Master Branch CSV'),
            
            # Core business records
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
                    self.stdout.write(f"Deleting {display_name}...")
                    try:
                        queryset.delete()
                        self.stdout.write(f"   ✓ Deleted {count} {display_name}")
                    except Exception as e:
                        self.stdout.write(f"   ⚠️  Warning: Could not delete {display_name}: {e}")
        
        # Finally delete the Branch
        self.stdout.write("Deleting Branch...")
        try:
            branch_name = branch.name
            branch_code = branch.code
            branch.delete()
            self.stdout.write(f"   ✓ Deleted Branch: {branch_code} - {branch_name}")
        except Exception as e:
            self.stdout.write(f"   ❌ Error deleting Branch: {e}")
            raise

    def _verify_cleanup(self):
        """Verify that all records were properly cleaned up."""
        self.stdout.write(f"\n=== VERIFICATION ===")
        
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
            self.stdout.write(f"Remaining {model_name}: {count}")
        
        # Check for any orphaned records
        orphaned_staff = Staff.objects.filter(branch__isnull=True).count()
        orphaned_users = Users.objects.filter(branch__isnull=True).count()
        
        if orphaned_staff > 0 or orphaned_users > 0:
            self.stdout.write(self.style.WARNING(f"Warning: {orphaned_staff} staff and {orphaned_users} users have no branch assigned"))
        else:
            self.stdout.write(self.style.SUCCESS("✓ All records properly cleaned up"))
