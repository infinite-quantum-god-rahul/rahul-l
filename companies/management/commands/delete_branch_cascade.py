from django.core.management.base import BaseCommand
from companies.models import Branch, Staff, Users, UserPermission

class Command(BaseCommand):
    help = "Delete a branch and all its related records (Staff, Users, UserPermissions)"

    def add_arguments(self, parser):
        parser.add_argument('branch_code', type=str, help='Branch code to delete (e.g., BRN001)')
        parser.add_argument('--force', action='store_true', help='Skip confirmation prompt')

    def handle(self, *args, **options):
        branch_code = options['branch_code']
        force = options['force']
        
        try:
            # Find the branch
            branch = Branch.objects.get(code=branch_code)
            
            self.stdout.write(f"Found branch: {branch.code} - {branch.name}")
            
            # Count related records
            staff_count = Staff.objects.filter(branch=branch).count()
            users_count = Users.objects.filter(branch=branch).count()
            
            # Find UserPermissions that reference Users from this branch
            users_in_branch = Users.objects.filter(branch=branch)
            up_count = UserPermission.objects.filter(user_profile__in=users_in_branch).count()
            
            self.stdout.write(f"\nRelated records to be deleted:")
            self.stdout.write(f"  - Staff: {staff_count}")
            self.stdout.write(f"  - Users: {users_count}")
            self.stdout.write(f"  - UserPermissions: {up_count}")
            
            if not force:
                confirm = input(f"\nAre you sure you want to delete branch '{branch.name}' and ALL related records? (yes/no): ")
                if confirm.lower() != 'yes':
                    self.stdout.write("Operation cancelled.")
                    return
            
            self.stdout.write(f"\n=== STARTING CASCADE DELETION ===")
            
            # Delete UserPermissions first (they reference Users)
            if up_count > 0:
                self.stdout.write("1. Deleting UserPermission records...")
                UserPermission.objects.filter(user_profile__in=users_in_branch).delete()
                self.stdout.write(f"   ✓ Deleted {up_count} UserPermission records")
            
            # Delete Users records
            if users_count > 0:
                self.stdout.write("2. Deleting Users records...")
                users_in_branch.delete()
                self.stdout.write(f"   ✓ Deleted {users_count} Users records")
            
            # Delete Staff records
            if staff_count > 0:
                self.stdout.write("3. Deleting Staff records...")
                Staff.objects.filter(branch=branch).delete()
                self.stdout.write(f"   ✓ Deleted {staff_count} Staff records")
            
            # Finally delete the Branch
            self.stdout.write("4. Deleting Branch...")
            branch_name = branch.name
            branch_code = branch.code
            branch.delete()
            self.stdout.write(f"   ✓ Deleted Branch: {branch_code} - {branch_name}")
            
            self.stdout.write(f"\n=== CASCADE DELETION COMPLETE ===")
            self.stdout.write(f"✓ Branch '{branch_name}' and all related records have been permanently deleted.")
            
            # Verify cleanup
            self.stdout.write(f"\n=== VERIFICATION ===")
            self.stdout.write(f"Remaining branches: {Branch.objects.count()}")
            self.stdout.write(f"Remaining staff: {Staff.objects.count()}")
            self.stdout.write(f"Remaining users: {Users.objects.count()}")
            self.stdout.write(f"Remaining user permissions: {UserPermission.objects.count()}")
            
        except Branch.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Branch with code '{branch_code}' not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            import traceback
            traceback.print_exc()
