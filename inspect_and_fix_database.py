#!/usr/bin/env python
"""
Comprehensive Database Inspection and Fix Script
This script will inspect your database and show exactly what's blocking branch deletion.
"""

import sqlite3
import os
import sys

def connect_to_database():
    """Connect to the SQLite database directly."""
    db_path = "db.sqlite3"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("Please run this script from the directory containing db.sqlite3")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print(f"✅ Connected to database: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def inspect_database_completely():
    """Completely inspect the database structure and content."""
    print("🔍 COMPREHENSIVE DATABASE INSPECTION")
    print("=" * 60)
    
    conn = connect_to_database()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row['name'] for row in cursor.fetchall()]
        
        print(f"Found {len(tables)} tables in database")
        print()
        
        # Inspect each table
        all_branch_references = []
        
        for table in tables:
            print(f"📋 Table: {table}")
            print("-" * 40)
            
            try:
                # Get table structure
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                
                branch_columns = []
                for col in columns:
                    col_name = col['name']
                    col_type = col['type']
                    not_null = col['notnull']
                    pk = col['pk']
                    
                    print(f"  Column: {col_name:<20} | Type: {col_type:<15} | NotNull: {not_null} | PK: {pk}")
                    
                    if 'branch' in col_name.lower():
                        branch_columns.append(col_name)
                
                # Check for branch references
                if branch_columns:
                    print(f"  🔍 Found branch columns: {', '.join(branch_columns)}")
                    
                    for col in branch_columns:
                        try:
                            cursor.execute(f"SELECT COUNT(*) as count FROM {table} WHERE {col} IS NOT NULL")
                            result = cursor.fetchone()
                            count = result['count']
                            
                            if count > 0:
                                print(f"    Records with {col}: {count}")
                                
                                # Get sample records
                                cursor.execute(f"SELECT * FROM {table} WHERE {col} IS NOT NULL LIMIT 3")
                                samples = cursor.fetchall()
                                
                                for i, sample in enumerate(samples, 1):
                                    print(f"      Sample {i}: {dict(sample)}")
                                
                                all_branch_references.append({
                                    'table': table,
                                    'column': col,
                                    'count': count,
                                    'samples': samples
                                })
                                
                        except Exception as e:
                            print(f"    Error checking {col}: {e}")
                
                print()
                
            except Exception as e:
                print(f"  ❌ Error examining table {table}: {e}")
                print()
        
        return all_branch_references
        
    finally:
        conn.close()

def find_specific_branch_issues(branch_code):
    """Find specific issues for a particular branch."""
    print(f"\n🔍 FINDING ISSUES FOR BRANCH: {branch_code}")
    print("=" * 60)
    
    conn = connect_to_database()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Find the branch
        cursor.execute("SELECT id, code, name FROM companies_branch WHERE code = ?", [branch_code])
        result = cursor.fetchone()
        
        if not result:
            print(f"❌ Branch '{branch_code}' not found")
            return None
        
        branch_id = result['id']
        branch_name = result['name']
        
        print(f"✅ Found branch: {branch_code} - {branch_name} (ID: {branch_id})")
        
        # Find all references to this specific branch
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in cursor.fetchall()]
        
        branch_issues = []
        
        for table in tables:
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                
                for col in columns:
                    col_name = col['name']
                    if 'branch' in col_name.lower():
                        # Check for records with this specific branch ID
                        try:
                            cursor.execute(f"SELECT COUNT(*) as count FROM {table} WHERE {col_name} = ?", [branch_id])
                            result = cursor.fetchone()
                            count = result['count']
                            
                            if count > 0:
                                print(f"  Found: {table}.{col_name} -> {count} records")
                                
                                # Get sample records
                                cursor.execute(f"SELECT * FROM {table} WHERE {col_name} = ? LIMIT 2", [branch_id])
                                samples = cursor.fetchall()
                                
                                for i, sample in enumerate(samples, 1):
                                    print(f"    Sample {i}: {dict(sample)}")
                                
                                branch_issues.append({
                                    'table': table,
                                    'column': col_name,
                                    'count': count,
                                    'samples': samples
                                })
                                
                        except Exception as e:
                            print(f"  Error checking {table}.{col_name}: {e}")
                            
            except Exception as e:
                print(f"Error examining table {table}: {e}")
        
        return branch_issues
        
    finally:
        conn.close()

def create_detailed_fix_script(branch_code, branch_issues):
    """Create a detailed fix script based on found issues."""
    print(f"\n🔧 CREATING DETAILED FIX SCRIPT")
    print("=" * 60)
    
    if not branch_issues:
        print("✅ No issues found - branch can be deleted safely")
        return None
    
    print(f"Found {len(branch_issues)} tables with records that need deletion")
    
    # Create the fix script
    script_content = f"""#!/usr/bin/env python
# Detailed Branch Deletion Fix Script for {branch_code}
# Generated automatically based on database inspection

import sqlite3
import os

def fix_branch_{branch_code.lower()}():
    \"\"\"Fix branch deletion issue for {branch_code}.\"\"\"
    print("🔧 FIXING BRANCH DELETION ISSUE FOR: {branch_code}")
    print("=" * 60)
    
    # Connect to database
    db_path = "db.sqlite3"
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {{db_path}}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Find branch ID
        cursor.execute("SELECT id, name FROM companies_branch WHERE code = ?", ["{branch_code}"])
        result = cursor.fetchone()
        if not result:
            print(f"❌ Branch '{branch_code}' not found")
            return False
        
        branch_id, branch_name = result[0], result[1]
        print(f"✅ Found branch: {{branch_name}} (ID: {{branch_id}})")
        
        # Disable foreign key constraints
        print("🔧 Disabling foreign key constraints...")
        cursor.execute("PRAGMA foreign_keys = OFF")
        print("✅ Constraints disabled")
        
        # Delete records from each problematic table
"""
    
    # Add deletion commands for each table
    for issue in branch_issues:
        table = issue['table']
        column = issue['column']
        count = issue['count']
        
        script_content += f"""
        # Delete from {table}
        print(f"Deleting from {table}...")
        try:
            cursor.execute("DELETE FROM {table} WHERE {column} = ?", [branch_id])
            deleted = cursor.rowcount
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
            if cursor.rowcount > 0:
                print(f"  ✅ Branch '{branch_code}' deleted successfully")
            else:
                print(f"  ❌ Failed to delete branch")
                return False
        except Exception as e:
            print(f"  ❌ Error deleting branch: {{e}}")
            return False
        
        # Re-enable constraints
        print("🔧 Re-enabling foreign key constraints...")
        cursor.execute("PRAGMA foreign_keys = ON")
        print("✅ Constraints re-enabled")
        
        # Verify deletion
        print("🔍 Verifying deletion...")
        cursor.execute("SELECT COUNT(*) FROM companies_branch WHERE code = ?", ["{branch_code}"])
        remaining = cursor.fetchone()[0]
        
        if remaining == 0:
            print("✅ Branch deletion verified successfully!")
            return True
        else:
            print(f"❌ Branch still exists ({{remaining}} records)")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {{e}}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        success = fix_branch_{branch_code.lower()}()
        if success:
            print("\\n🎉 SUCCESS: Branch deletion issue has been fixed!")
            print("You can now delete the branch through your normal method.")
        else:
            print("\\n❌ FAILED: Could not fix the branch deletion issue")
    except Exception as e:
        print(f"\\n❌ Unexpected error: {{e}}")
        import traceback
        traceback.print_exc()
"""
    
    # Write the script to file
    script_filename = f"fix_branch_{branch_code.lower()}_detailed.py"
    with open(script_filename, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Created detailed fix script: {script_filename}")
    print(f"Run it with: python {script_filename}")
    
    return script_filename

def main():
    """Main function."""
    print("🔧 COMPREHENSIVE DATABASE INSPECTION AND FIX")
    print("This script will inspect your database and create a targeted fix")
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python inspect_and_fix_database.py <BRANCH_CODE>")
        print("Example: python inspect_and_fix_database.py BRN001")
        return
    
    branch_code = sys.argv[1]
    
    try:
        # First, do a complete database inspection
        print("🔍 Step 1: Complete database inspection...")
        all_references = inspect_database_completely()
        
        if all_references:
            print(f"\n📊 Found {len(all_references)} tables with branch references:")
            for ref in all_references:
                print(f"  {ref['table']} ({ref['column']}): {ref['count']} records")
        
        print(f"\n🔍 Step 2: Finding specific issues for branch '{branch_code}'...")
        branch_issues = find_specific_branch_issues(branch_code)
        
        if branch_issues:
            print(f"\n⚠️  Found {len(branch_issues)} issues blocking branch deletion:")
            for issue in branch_issues:
                print(f"  {issue['table']} ({issue['column']}): {issue['count']} records")
            
            print(f"\n🔧 Step 3: Creating detailed fix script...")
            script_file = create_detailed_fix_script(branch_code, branch_issues)
            
            print(f"\n🎯 SOLUTION:")
            print(f"1. Run the generated script: python {script_file}")
            print(f"2. This will fix the constraint issue permanently")
            print(f"3. You can then delete the branch normally")
            
        else:
            print(f"\n✅ No issues found for branch '{branch_code}'")
            print("The branch should be deletable through normal means.")
            
    except Exception as e:
        print(f"❌ Error during inspection: {e}")
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
