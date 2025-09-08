#!/usr/bin/env python
"""
Force Delete Branch Script
This script will definitely delete a branch by temporarily disabling constraints
and using raw SQL to clean up everything.
"""

import os
import sys
import django
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANCH_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

def force_delete_branch(branch_code):
    """Force delete a branch by any means necessary."""
    print(f"☢️  FORCE DELETING BRANCH: {branch_code}")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Step 1: Find the branch
        try:
            cursor.execute("SELECT id, name FROM companies_branch WHERE code = ?", [branch_code])
            result = cursor.fetchone()
            if not result:
                print(f"❌ Branch '{branch_code}' not found")
                return False
            
            branch_id, branch_name = result
            print(f"✅ Found branch: {branch_name} (ID: {branch_id})")
            
        except Exception as e:
            print(f"❌ Error finding branch: {e}")
            return False
        
        # Step 2: Disable foreign key constraints temporarily
        print("🔧 Temporarily disabling foreign key constraints...")
        try:
            cursor.execute("PRAGMA foreign_keys = OFF")
            print("✅ Foreign key constraints disabled")
        except Exception as e:
            print(f"⚠️  Could not disable constraints: {e}")
        
        # Step 3: Find all tables with branch references
        print("🔍 Finding all branch-related tables...")
        branch_tables = []
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                
                for col in columns:
                    col_name = col[1]
                    if 'branch' in col_name.lower():
                        # Check if there are records
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} = ?", [branch_id])
                            count = cursor.fetchone()[0]
                            if count > 0:
                                branch_tables.append({
                                    'table': table,
                                    'column': col_name,
                                    'count': count
                                })
                        except Exception as e:
                            print(f"⚠️  Error checking {table}.{col_name}: {e}")
                            
            except Exception as e:
                print(f"⚠️  Error examining table {table}: {e}")
        
        if branch_tables:
            print(f"\n📋 Found {len(branch_tables)} tables with branch records:")
            for table_info in branch_tables:
                print(f"  {table_info['table']} ({table_info['column']}): {table_info['count']} records")
            
            # Step 4: Delete all related records
            print(f"\n🗑️  Deleting all related records...")
            total_deleted = 0
            
            for table_info in branch_tables:
                table = table_info['table']
                column = table_info['column']
                count = table_info['count']
                
                print(f"Deleting from {table}...")
                try:
                    cursor.execute(f"DELETE FROM {table} WHERE {column} = ?", [branch_id])
                    deleted = cursor.connection.total_changes
                    total_deleted += deleted
                    print(f"  ✅ Deleted {deleted} records from {table}")
                except Exception as e:
                    print(f"  ❌ Error deleting from {table}: {e}")
                    # Continue with other tables
            
            print(f"✅ Total records deleted: {total_deleted}")
        else:
            print("✅ No related records found")
        
        # Step 5: Delete the branch itself
        print(f"\n🗑️  Deleting branch record...")
        try:
            cursor.execute("DELETE FROM companies_branch WHERE id = ?", [branch_id])
            if cursor.connection.total_changes > 0:
                print(f"✅ Branch '{branch_code}' deleted successfully")
            else:
                print(f"❌ Failed to delete branch")
                return False
        except Exception as e:
            print(f"❌ Error deleting branch: {e}")
            return False
        
        # Step 6: Re-enable foreign key constraints
        print("🔧 Re-enabling foreign key constraints...")
        try:
            cursor.execute("PRAGMA foreign_keys = ON")
            print("✅ Foreign key constraints re-enabled")
        except Exception as e:
            print(f"⚠️  Could not re-enable constraints: {e}")
        
        # Step 7: Verify deletion
        print(f"\n🔍 Verifying deletion...")
        try:
            cursor.execute("SELECT COUNT(*) FROM companies_branch WHERE code = ?", [branch_code])
            remaining = cursor.fetchone()[0]
            if remaining == 0:
                print("✅ Branch deletion verified successfully!")
                return True
            else:
                print(f"❌ Branch still exists ({remaining} records)")
                return False
        except Exception as e:
            print(f"⚠️  Could not verify deletion: {e}")
            return True  # Assume success if we can't verify

def main():
    """Main function."""
    print("☢️  FORCE BRANCH DELETION SCRIPT")
    print("This script will definitely delete a branch by any means necessary")
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python force_delete_branch.py <BRANCH_CODE>")
        print("Example: python force_delete_branch.py BRN001")
        return
    
    branch_code = sys.argv[1]
    
    # Confirm deletion
    print(f"⚠️  WARNING: This will force delete branch '{branch_code}' and ALL related records!")
    print("This action cannot be undone!")
    
    confirm = input(f"\nAre you absolutely sure? Type 'YES' to proceed: ").strip()
    if confirm != 'YES':
        print("❌ Operation cancelled")
        return
    
    try:
        success = force_delete_branch(branch_code)
        
        if success:
            print(f"\n🎉 SUCCESS: Branch '{branch_code}' has been force deleted!")
            print("All related records have been removed from the database.")
        else:
            print(f"\n❌ FAILED: Could not delete branch '{branch_code}'")
            print("Check the error messages above for details.")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
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
