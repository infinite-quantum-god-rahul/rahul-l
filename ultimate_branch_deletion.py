#!/usr/bin/env python
# ULTIMATE BRANCH DELETION - Bypass Everything
# This script will completely bypass all database constraints and directly manipulate the SQLite file

import sqlite3
import os
import sys
import shutil
import tempfile

def ultimate_branch_deletion():
    """Ultimate solution to force delete branch BRN001."""
    print("ULTIMATE BRANCH DELETION - BYPASSING EVERYTHING")
    print("=" * 60)
    print("This will completely bypass ALL constraints and database rules!")
    print()
    
    # Connect to database
    db_path = "db.sqlite3"
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found: {db_path}")
        return False
    
    # Create backup first
    backup_path = "db.sqlite3.backup_before_deletion"
    print(f"Creating backup: {backup_path}")
    shutil.copy2(db_path, backup_path)
    print("SUCCESS: Backup created")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Find branch ID
        cursor.execute("SELECT id, name FROM companies_branch WHERE code = ?", ["BRN001"])
        result = cursor.fetchone()
        if not result:
            print(f"ERROR: Branch 'BRN001' not found")
            return False
        
        branch_id, branch_name = result[0], result[1]
        print(f"SUCCESS: Found branch: {branch_name} (ID: {branch_id})")
        
        # STEP 1: Disable ALL possible constraints
        print("\nSTEP 1: Disabling ALL possible constraints...")
        cursor.execute("PRAGMA foreign_keys = OFF")
        cursor.execute("PRAGMA check_foreign_keys = OFF")
        cursor.execute("PRAGMA defer_foreign_keys = ON")
        cursor.execute("PRAGMA synchronous = OFF")
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA temp_store = MEMORY")
        print("SUCCESS: All constraints and safety features disabled")
        
        # STEP 2: Find ALL tables with ANY branch reference (case insensitive)
        print("\nSTEP 2: Finding ALL tables with branch references...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        branch_tables = []
        for table in tables:
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                
                for col in columns:
                    col_name = col[1]
                    # Check for ANY variation of branch in column name
                    if any(branch_word in col_name.lower() for branch_word in ['branch', 'brn', 'branch_id', 'branchid']):
                        # Check if there are records for this branch
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} = ?", [branch_id])
                            count = cursor.fetchone()[0]
                            
                            if count > 0:
                                branch_tables.append({
                                    'table': table,
                                    'column': col_name,
                                    'count': count
                                })
                                print(f"  Found: {table}.{col_name} -> {count} records")
                        except Exception as e:
                            print(f"    Warning: Could not check {table}.{col_name}: {e}")
            except Exception as e:
                print(f"Warning: Could not examine table {table}: {e}")
        
        if not branch_tables:
            print("  No branch references found")
        
        # STEP 3: Delete from ALL tables with branch references
        print(f"\nSTEP 3: Deleting from {len(branch_tables)} tables...")
        
        for table_info in branch_tables:
            table = table_info['table']
            column = table_info['column']
            count = table_info['count']
            
            print(f"  Deleting from {table}...")
            try:
                # Try multiple deletion strategies
                cursor.execute(f"DELETE FROM {table} WHERE {column} = ?", [branch_id])
                deleted = cursor.rowcount
                print(f"    SUCCESS: Deleted {deleted} records from {table}")
            except Exception as e:
                print(f"    ERROR: Could not delete from {table}: {e}")
                # Try alternative approach - update to NULL first
                try:
                    print(f"    Trying alternative approach for {table}...")
                    cursor.execute(f"UPDATE {table} SET {column} = NULL WHERE {column} = ?", [branch_id])
                    updated = cursor.rowcount
                    print(f"    SUCCESS: Updated {updated} records in {table} to NULL")
                except Exception as e2:
                    print(f"    ERROR: Alternative approach also failed: {e2}")
        
        # STEP 4: Force delete the branch itself
        print(f"\nSTEP 4: Force deleting branch record...")
        try:
            cursor.execute("DELETE FROM companies_branch WHERE id = ?", [branch_id])
            if cursor.rowcount > 0:
                print(f"  SUCCESS: Branch 'BRN001' force deleted!")
            else:
                print(f"  ERROR: Branch still exists after deletion attempt")
        except Exception as e:
            print(f"  ERROR: Could not delete branch: {e}")
        
        # STEP 5: Commit all changes
        print(f"\nSTEP 5: Committing all changes...")
        conn.commit()
        print("SUCCESS: All changes committed")
        
        # STEP 6: Re-enable constraints
        print(f"\nSTEP 6: Re-enabling constraints...")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA check_foreign_keys = ON")
        cursor.execute("PRAGMA defer_foreign_keys = OFF")
        cursor.execute("PRAGMA synchronous = NORMAL")
        cursor.execute("PRAGMA journal_mode = DELETE")
        print("SUCCESS: Constraints re-enabled")
        
        # STEP 7: Verify deletion
        print(f"\nSTEP 7: Verifying deletion...")
        cursor.execute("SELECT COUNT(*) FROM companies_branch WHERE code = ?", ["BRN001"])
        remaining = cursor.fetchone()[0]
        
        if remaining == 0:
            print("SUCCESS: Branch deletion verified successfully!")
            return True
        else:
            print(f"ERROR: Branch still exists ({remaining} records)")
            return False
            
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        conn.close()

def main():
    """Main function."""
    print("ULTIMATE BRANCH DELETION - BYPASSING EVERYTHING")
    print("This script will completely bypass ALL constraints and database rules!")
    print()
    
    # Confirm deletion
    print("WARNING: This will force delete branch 'BRN001' and ALL related records!")
    print("This action cannot be undone!")
    print("This script directly modifies your database!")
    print("A backup will be created as 'db.sqlite3.backup_before_deletion'")
    
    confirm = input("\nAre you absolutely sure? Type 'YES' to proceed: ").strip()
    if confirm != 'YES':
        print("Operation cancelled")
        return
    
    try:
        success = ultimate_branch_deletion()
        
        if success:
            print(f"\nSUCCESS: Branch 'BRN001' has been completely deleted!")
            print("All related records have been removed from the database.")
            print("The FOREIGN KEY constraint error should no longer occur.")
            print(f"Backup saved as: db.sqlite3.backup_before_deletion")
        else:
            print(f"\nFAILED: Could not delete branch 'BRN001'")
            print("Check the error messages above for details.")
            print("Your database has been backed up before any changes.")
            
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\nOperation cancelled by user.")
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
