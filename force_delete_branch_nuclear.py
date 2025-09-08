#!/usr/bin/env python
# NUCLEAR OPTION - Force Delete Branch BRN001
# This script will completely bypass all constraints and force deletion

import sqlite3
import os
import sys

def force_delete_branch_nuclear():
    """Nuclear option to force delete branch BRN001."""
    print("NUCLEAR OPTION - FORCE DELETING BRANCH BRN001")
    print("=" * 60)
    print("This will completely bypass all constraints!")
    print()
    
    # Connect to database
    db_path = "db.sqlite3"
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found: {db_path}")
        return False
    
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
        
        # STEP 1: Disable ALL constraints
        print("\nSTEP 1: Disabling ALL constraints...")
        cursor.execute("PRAGMA foreign_keys = OFF")
        cursor.execute("PRAGMA check_foreign_keys = OFF")
        cursor.execute("PRAGMA defer_foreign_keys = ON")
        print("SUCCESS: All constraints disabled")
        
        # STEP 2: Find ALL tables with ANY branch reference
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
                    if 'branch' in col_name.lower():
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
                        except:
                            pass
            except:
                pass
        
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
                cursor.execute(f"DELETE FROM {table} WHERE {column} = ?", [branch_id])
                deleted = cursor.rowcount
                print(f"    SUCCESS: Deleted {deleted} records from {table}")
            except Exception as e:
                print(f"    ERROR: Could not delete from {table}: {e}")
                # Continue anyway - this is nuclear option
        
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
        
        # STEP 5: Re-enable constraints
        print(f"\nSTEP 5: Re-enabling constraints...")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA check_foreign_keys = ON")
        cursor.execute("PRAGMA defer_foreign_keys = OFF")
        print("SUCCESS: Constraints re-enabled")
        
        # STEP 6: Verify deletion
        print(f"\nSTEP 6: Verifying deletion...")
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
    print("NUCLEAR OPTION - FORCE BRANCH DELETION")
    print("This script will completely bypass all constraints!")
    print()
    
    # Confirm deletion
    print("WARNING: This will force delete branch 'BRN001' and ALL related records!")
    print("This action cannot be undone!")
    print("This script directly modifies your database!")
    
    confirm = input("\nAre you absolutely sure? Type 'YES' to proceed: ").strip()
    if confirm != 'YES':
        print("Operation cancelled")
        return
    
    try:
        success = force_delete_branch_nuclear()
        
        if success:
            print(f"\nSUCCESS: Branch 'BRN001' has been completely deleted!")
            print("All related records have been removed from the database.")
            print("The FOREIGN KEY constraint error should no longer occur.")
        else:
            print(f"\nFAILED: Could not delete branch 'BRN001'")
            print("Check the error messages above for details.")
            
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
