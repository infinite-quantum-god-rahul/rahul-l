#!/usr/bin/env python
"""
Debug Branch Deletion Issues
This script directly inspects the database to find the exact constraint issue
and provides a targeted solution.
"""

import os
import sys
import django
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

def inspect_database_structure():
    """Inspect the database structure to understand the issue."""
    print("🔍 INSPECTING DATABASE STRUCTURE")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Get all tables
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
    
    print(f"Found {len(tables)} tables in database")
    
    # Look for branch-related tables
    branch_tables = []
    for table in tables:
        try:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            branch_columns = []
            for col in columns:
                col_name = col[1]
                if 'branch' in col_name.lower():
                    branch_columns.append(col_name)
            
            if branch_columns:
                branch_tables.append({
                    'table': table,
                    'columns': branch_columns
                })
                
        except Exception as e:
            print(f"⚠️  Error examining table {table}: {e}")
    
    return branch_tables

def find_constraint_issues(branch_code):
    """Find specific constraint issues for a branch."""
    print(f"\n🔍 FINDING CONSTRAINT ISSUES FOR BRANCH: {branch_code}")
    print("=" * 60)
    
    # First, find the branch ID
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT id, name FROM companies_branch WHERE code = ?", [branch_code])
            result = cursor.fetchone()
            if not result:
                print(f"❌ Branch '{branch_code}' not found")
                return None
            
            branch_id, branch_name = result
            print(f"✅ Found branch: {branch_code} - {branch_name} (ID: {branch_id})")
            
        except Exception as e:
            print(f"❌ Error finding branch: {e}")
            return None
    
    # Get all branch-related tables
    branch_tables = inspect_database_structure()
    
    if not branch_tables:
        print("✅ No branch-related tables found")
        return None
    
    print(f"\n📋 BRANCH-RELATED TABLES:")
    print("-" * 50)
    
    constraint_issues = []
    
    for table_info in branch_tables:
        table = table_info['table']
        columns = table_info['columns']
        
        print(f"\nTable: {table}")
        for col in columns:
            try:
                # Count records for this branch
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} = ?", [branch_id])
                count = cursor.fetchone()[0]
                
                print(f"  Column: {col} -> {count} records")
                
                if count > 0:
                    constraint_issues.append({
                        'table': table,
                        'column': col,
                        'count': count
                    })
                    
            except Exception as e:
                print(f"  Column: {col} -> Error: {e}")
    
    return constraint_issues

def create_targeted_deletion_script(branch_code, constraint_issues):
    """Create a targeted deletion script based on found issues."""
    print(f"\n🔧 CREATING TARGETED DELETION SCRIPT")
    print("=" * 60)
    
    if not constraint_issues:
        print("✅ No constraint issues found - branch can be deleted safely")
        return
    
    print(f"Found {len(constraint_issues)} tables with records that need deletion")
    
    # Create the deletion script
    script_content = f"""#!/usr/bin/env python
# Targeted Branch Deletion Script for {branch_code}
# Generated automatically based on database inspection

import os
import sys
import django
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANCH_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

def delete_branch_{branch_code.lower()}():
    \"\"\"Delete branch {branch_code} and all related records.\"\"\"
    print("🗑️  DELETING BRANCH: {branch_code}")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Find branch ID
        cursor.execute("SELECT id, name FROM companies_branch WHERE code = ?", ["{branch_code}"])
        result = cursor.fetchone()
        if not result:
            print(f"❌ Branch '{branch_code}' not found")
            return False
        
        branch_id, branch_name = result
        print(f"✅ Found branch: {branch_name} (ID: {branch_id})")
        
        # Delete related records in order
"""
    
    # Add deletion commands for each table
    for issue in constraint_issues:
        table = issue['table']
        column = issue['column']
        count = issue['count']
        
        script_content += f"""
        # Delete from {table}
        print(f"Deleting from {table}...")
        try:
            cursor.execute("DELETE FROM {table} WHERE {column} = ?", [branch_id])
            deleted = cursor.connection.total_changes
            print(f"  ✅ Deleted {{deleted}} records from {table}")
        except Exception as e:
            print(f"  ❌ Error deleting from {table}: {{e}}")
            return False
"""
    
    # Add final branch deletion
    script_content += f"""
        # Finally delete the branch
        print("Deleting branch record...")
        try:
            cursor.execute("DELETE FROM companies_branch WHERE id = ?", [branch_id])
            if cursor.connection.total_changes > 0:
                print(f"  ✅ Branch '{branch_code}' deleted successfully")
                return True
            else:
                print(f"  ❌ Failed to delete branch")
                return False
        except Exception as e:
            print(f"  ❌ Error deleting branch: {{e}}")
            return False

if __name__ == "__main__":
    try:
        success = delete_branch_{branch_code.lower()}()
        if success:
            print("\\n✅ Branch deletion completed successfully!")
        else:
            print("\\n❌ Branch deletion failed!")
    except Exception as e:
        print(f"\\n❌ Unexpected error: {{e}}")
        import traceback
        traceback.print_exc()
"""
    
    # Write the script to file
    script_filename = f"delete_branch_{branch_code.lower()}_targeted.py"
    with open(script_filename, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Created targeted deletion script: {script_filename}")
    print(f"Run it with: python {script_filename}")
    
    return script_filename

def test_branch_deletion(branch_code):
    """Test if branch can be deleted by checking constraints."""
    print(f"\n🧪 TESTING BRANCH DELETION FOR: {branch_code}")
    print("=" * 60)
    
    constraint_issues = find_constraint_issues(branch_code)
    
    if not constraint_issues:
        print("✅ Branch can be deleted safely - no related records found")
        return True
    
    print(f"⚠️  Branch has {len(constraint_issues)} related tables with records")
    
    # Create targeted deletion script
    script_file = create_targeted_deletion_script(branch_code, constraint_issues)
    
    print(f"\n🔧 SOLUTION:")
    print(f"1. Run the generated script: python {script_file}")
    print(f"2. Or use the nuclear option: python nuclear_branch_deletion.py {branch_code} --execute")
    
    return False

def main():
    """Main function."""
    print("🔧 BRANCH DELETION DEBUGGER")
    print("This script will find the exact constraint issue and provide a solution")
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python debug_branch_deletion.py <BRANCH_CODE>")
        print("Example: python debug_branch_deletion.py BRN001")
        return
    
    branch_code = sys.argv[1]
    
    try:
        # Test the branch deletion
        can_delete = test_branch_deletion(branch_code)
        
        if can_delete:
            print(f"\n🎉 SUCCESS: Branch '{branch_code}' can be deleted safely!")
        else:
            print(f"\n⚠️  ACTION REQUIRED: Branch '{branch_code}' has related records that need deletion first")
            
    except Exception as e:
        print(f"❌ Error during debugging: {e}")
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
