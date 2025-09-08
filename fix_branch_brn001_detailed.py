#!/usr/bin/env python
# Detailed Branch Deletion Fix Script for BRN001
# Generated automatically based on database inspection

import sqlite3
import os

def fix_branch_brn001():
    """Fix branch deletion issue for BRN001."""
    print("FIXING BRANCH DELETION ISSUE FOR: BRN001")
    print("=" * 60)
    
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
        
        # Disable foreign key constraints
        print("Disabling foreign key constraints...")
        cursor.execute("PRAGMA foreign_keys = OFF")
        print("SUCCESS: Constraints disabled")
        
        # Delete records from each problematic table
        
        # Delete from companies_cadre
        print(f"Deleting from companies_cadre...")
        try:
            cursor.execute("DELETE FROM companies_cadre WHERE branch_id = ?", [branch_id])
            deleted = cursor.rowcount
            print(f"  SUCCESS: Deleted {deleted} records from companies_cadre")
        except Exception as e:
            print(f"  ERROR: Error deleting from companies_cadre: {e}")
            return False
        
        # Delete from companies_staff
        print(f"Deleting from companies_staff...")
        try:
            cursor.execute("DELETE FROM companies_staff WHERE branch_id = ?", [branch_id])
            deleted = cursor.rowcount
            print(f"  SUCCESS: Deleted {deleted} records from companies_staff")
        except Exception as e:
            print(f"  ERROR: Error deleting from companies_staff: {e}")
            return False
        
        # Delete from companies_userprofile
        print(f"Deleting from companies_userprofile...")
        try:
            cursor.execute("DELETE FROM companies_userprofile WHERE branch_id = ?", [branch_id])
            deleted = cursor.rowcount
            print(f"  SUCCESS: Deleted {deleted} records from companies_userprofile")
        except Exception as e:
            print(f"  ERROR: Error deleting from companies_userprofile: {e}")
            return False
        
        # Delete from companies_users
        print(f"Deleting from companies_users...")
        try:
            cursor.execute("DELETE FROM companies_users WHERE branch = ?", [branch_id])
            deleted = cursor.rowcount
            print(f"  SUCCESS: Deleted {deleted} records from companies_users")
        except Exception as e:
            print(f"  ERROR: Error deleting from companies_users: {e}")
            return False
        
        # Finally delete the branch
        print("Deleting branch record...")
        try:
            cursor.execute("DELETE FROM companies_branch WHERE id = ?", [branch_id])
            if cursor.rowcount > 0:
                print(f"  SUCCESS: Branch 'BRN001' deleted successfully")
            else:
                print(f"  ERROR: Failed to delete branch")
                return False
        except Exception as e:
            print(f"  ERROR: Error deleting branch: {e}")
            return False
        
        # Re-enable constraints
        print("Re-enabling foreign key constraints...")
        cursor.execute("PRAGMA foreign_keys = ON")
        print("SUCCESS: Constraints re-enabled")
        
        # Verify deletion
        print("Verifying deletion...")
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

if __name__ == "__main__":
    try:
        success = fix_branch_brn001()
        if success:
            print("\nSUCCESS: Branch deletion issue has been fixed!")
            print("You can now delete the branch through your normal method.")
        else:
            print("\nFAILED: Could not fix the branch deletion issue")
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
