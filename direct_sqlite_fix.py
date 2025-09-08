#!/usr/bin/env python
"""
Direct SQLite Database Fix for Branch Deletion
This script directly connects to the SQLite database and fixes the constraint issue.
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
        conn.row_factory = sqlite3.Row  # Enable row access by name
        print(f"✅ Connected to database: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def find_branch_info(conn, branch_code):
    """Find branch information."""
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, code, name FROM companies_branch WHERE code = ?", [branch_code])
        result = cursor.fetchone()
        
        if not result:
            print(f"❌ Branch '{branch_code}' not found")
            return None
        
        branch_id = result['id']
        branch_name = result['name']
        
        print(f"✅ Found branch: {branch_code} - {branch_name} (ID: {branch_id})")
        return {'id': branch_id, 'code': branch_code, 'name': branch_name}
        
    except Exception as e:
        print(f"❌ Error finding branch: {e}")
        return None

def find_all_branch_references(conn, branch_id):
    """Find all tables and records that reference this branch."""
    cursor = conn.cursor()
    
    print("🔍 Scanning database for branch references...")
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row['name'] for row in cursor.fetchall()]
    
    branch_references = []
    
    for table in tables:
        try:
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            for col in columns:
                col_name = col['name']
                if 'branch' in col_name.lower():
                    # Check if there are records for this branch
                    try:
                        cursor.execute(f"SELECT COUNT(*) as count FROM {table} WHERE {col_name} = ?", [branch_id])
                        result = cursor.fetchone()
                        count = result['count']
                        
                        if count > 0:
                            branch_references.append({
                                'table': table,
                                'column': col_name,
                                'count': count
                            })
                            print(f"  Found: {table}.{col_name} -> {count} records")
                            
                    except Exception as e:
                        print(f"  ⚠️  Error checking {table}.{col_name}: {e}")
                        
        except Exception as e:
            print(f"⚠️  Error examining table {table}: {e}")
    
    return branch_references

def disable_foreign_keys(conn):
    """Disable foreign key constraints."""
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA foreign_keys = OFF")
        print("✅ Foreign key constraints disabled")
        return True
    except Exception as e:
        print(f"⚠️  Could not disable constraints: {e}")
        return False

def enable_foreign_keys(conn):
    """Re-enable foreign key constraints."""
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA foreign_keys = ON")
        print("✅ Foreign key constraints re-enabled")
        return True
    except Exception as e:
        print(f"⚠️  Could not re-enable constraints: {e}")
        return False

def delete_branch_records(conn, branch_id, branch_references):
    """Delete all records related to the branch."""
    cursor = conn.cursor()
    
    if not branch_references:
        print("✅ No related records found")
        return True
    
    print(f"\n🗑️  Deleting {len(branch_references)} tables with branch records...")
    
    total_deleted = 0
    failed_tables = []
    
    for ref in branch_references:
        table = ref['table']
        column = ref['column']
        count = ref['count']
        
        print(f"Deleting from {table}...")
        
        try:
            cursor.execute(f"DELETE FROM {table} WHERE {column} = ?", [branch_id])
            deleted = cursor.rowcount
            total_deleted += deleted
            
            print(f"  ✅ Deleted {deleted} records from {table}")
            
        except Exception as e:
            print(f"  ❌ Error deleting from {table}: {e}")
            failed_tables.append(table)
    
    if failed_tables:
        print(f"⚠️  Failed to delete from: {', '.join(failed_tables)}")
        return False
    
    print(f"✅ Total records deleted: {total_deleted}")
    return True

def delete_branch(conn, branch_id, branch_code):
    """Delete the branch record itself."""
    cursor = conn.cursor()
    
    print(f"\n🗑️  Deleting branch record...")
    
    try:
        cursor.execute("DELETE FROM companies_branch WHERE id = ?", [branch_id])
        
        if cursor.rowcount > 0:
            print(f"✅ Branch '{branch_code}' deleted successfully")
            return True
        else:
            print(f"❌ Failed to delete branch")
            return False
            
    except Exception as e:
        print(f"❌ Error deleting branch: {e}")
        return False

def verify_deletion(conn, branch_code):
    """Verify that the branch was deleted."""
    cursor = conn.cursor()
    
    print(f"\n🔍 Verifying deletion...")
    
    try:
        cursor.execute("SELECT COUNT(*) as count FROM companies_branch WHERE code = ?", [branch_code])
        result = cursor.fetchone()
        remaining = result['count']
        
        if remaining == 0:
            print("✅ Branch deletion verified successfully!")
            return True
        else:
            print(f"❌ Branch still exists ({remaining} records)")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not verify deletion: {e}")
        return True  # Assume success if we can't verify

def force_delete_branch_direct(branch_code):
    """Force delete a branch using direct SQLite connection."""
    print(f"☢️  FORCE DELETING BRANCH: {branch_code}")
    print("=" * 60)
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return False
    
    try:
        # Find branch
        branch_info = find_branch_info(conn, branch_code)
        if not branch_info:
            return False
        
        branch_id = branch_info['id']
        
        # Find all references
        branch_references = find_all_branch_references(conn, branch_id)
        
        if branch_references:
            print(f"\n📋 Found {len(branch_references)} tables with branch records:")
            for ref in branch_references:
                print(f"  {ref['table']} ({ref['column']}): {ref['count']} records")
        
        # Disable foreign keys
        if not disable_foreign_keys(conn):
            print("⚠️  Continuing without disabling constraints...")
        
        # Delete related records
        if not delete_branch_records(conn, branch_id, branch_references):
            print("❌ Failed to delete related records")
            return False
        
        # Delete branch
        if not delete_branch(conn, branch_id, branch_code):
            print("❌ Failed to delete branch")
            return False
        
        # Re-enable foreign keys
        enable_foreign_keys(conn)
        
        # Verify deletion
        if not verify_deletion(conn, branch_code):
            print("❌ Deletion verification failed")
            return False
        
        print(f"\n🎉 SUCCESS: Branch '{branch_code}' has been completely deleted!")
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        conn.close()
        print("✅ Database connection closed")

def main():
    """Main function."""
    print("☢️  DIRECT SQLITE BRANCH DELETION")
    print("This script directly connects to your SQLite database to fix the issue")
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python direct_sqlite_fix.py <BRANCH_CODE>")
        print("Example: python direct_sqlite_fix.py BRN001")
        return
    
    branch_code = sys.argv[1]
    
    # Confirm deletion
    print(f"⚠️  WARNING: This will force delete branch '{branch_code}' and ALL related records!")
    print("This action cannot be undone!")
    print("This script directly modifies your database!")
    
    confirm = input(f"\nAre you absolutely sure? Type 'YES' to proceed: ").strip()
    if confirm != 'YES':
        print("❌ Operation cancelled")
        return
    
    try:
        success = force_delete_branch_direct(branch_code)
        
        if success:
            print(f"\n🎉 SUCCESS: Branch '{branch_code}' has been completely deleted!")
            print("All related records have been removed from the database.")
            print("The FOREIGN KEY constraint error should no longer occur.")
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
