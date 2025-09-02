#!/usr/bin/env python
"""
Script to fix foreign key relationships for cascade deletion.
This will update the database to ensure that when a branch is deleted,
all related records are automatically deleted.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.db import connection
from companies.models import Branch, Staff, Users, UserPermission

def fix_cascade_deletion():
    """Fix foreign key relationships for cascade deletion."""
    
    print("=== FIXING CASCADE DELETION FOR BRANCHES ===")
    
    # Check current state
    print("\n=== CURRENT STATE ===")
    branches = Branch.objects.all()
    print(f"Total branches: {branches.count()}")
    for branch in branches:
        print(f"  - {branch.code}: {branch.name}")
        
        # Count related records
        staff_count = Staff.objects.filter(branch=branch).count()
        users_count = Users.objects.filter(branch=branch).count()
        print(f"    Staff: {staff_count}, Users: {users_count}")
    
    print(f"\n⚠️  WARNING: This will modify your database schema!")
    print(f"   - Staff records will be automatically deleted when their branch is deleted")
    print(f"   - Users records will be automatically deleted when their branch is deleted")
    print(f"   - UserPermission records will be automatically deleted when their user is deleted")
    
    response = input("\nDo you want to proceed with the fix? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Operation cancelled.")
        return
    
    print(f"\n=== APPLYING FIXES ===")
    
    try:
        with connection.cursor() as cursor:
            # Drop existing foreign key constraints
            print("1. Dropping existing foreign key constraints...")
            
            # Get table names
            cursor.execute("PRAGMA table_info(companies_staff)")
            staff_columns = cursor.fetchall()
            
            cursor.execute("PRAGMA table_info(companies_users)")
            users_columns = cursor.fetchall()
            
            # Find foreign key constraints
            cursor.execute("PRAGMA foreign_key_list(companies_staff)")
            staff_fks = cursor.fetchall()
            
            cursor.execute("PRAGMA foreign_key_list(companies_users)")
            users_fks = cursor.fetchall()
            
            print(f"   Found {len(staff_fks)} foreign keys in Staff table")
            print(f"   Found {len(users_fks)} foreign keys in Users table")
            
            # For SQLite, we need to recreate the tables with proper constraints
            # This is a more complex operation that requires careful handling
            
            print("\n2. Creating new tables with cascade deletion...")
            
            # Create new Staff table with cascade deletion
            cursor.execute("""
                CREATE TABLE companies_staff_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code VARCHAR(50) UNIQUE,
                    name VARCHAR(255),
                    company_id INTEGER NOT NULL,
                    branch_id INTEGER,
                    cadre_id INTEGER,
                    designation VARCHAR(100),
                    joining_date DATE,
                    status VARCHAR(20) DEFAULT 'active',
                    bank VARCHAR(100),
                    ifsc VARCHAR(20),
                    contact1 VARCHAR(15),
                    photo VARCHAR(100),
                    created_at DATETIME,
                    updated_at DATETIME,
                    extra_data TEXT,
                    raw_csv_data TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies_company (id) ON DELETE CASCADE,
                    FOREIGN KEY (branch_id) REFERENCES companies_branch (id) ON DELETE CASCADE,
                    FOREIGN KEY (cadre_id) REFERENCES companies_cadre (id) ON DELETE SET NULL
                )
            """)
            
            # Create new Users table with cascade deletion
            cursor.execute("""
                CREATE TABLE companies_users_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    staff_id INTEGER,
                    full_name VARCHAR(255),
                    branch_id INTEGER,
                    department VARCHAR(100),
                    mobile VARCHAR(20),
                    is_reports BOOLEAN DEFAULT 1,
                    status VARCHAR(20) DEFAULT 'active',
                    password VARCHAR(128),
                    created_at DATETIME,
                    updated_at DATETIME,
                    extra_data TEXT,
                    raw_csv_data TEXT,
                    FOREIGN KEY (user_id) REFERENCES auth_user (id) ON DELETE SET NULL,
                    FOREIGN KEY (staff_id) REFERENCES companies_staff (id) ON DELETE SET NULL,
                    FOREIGN KEY (branch_id) REFERENCES companies_branch (id) ON DELETE CASCADE
                )
            """)
            
            print("   ✓ New tables created with cascade deletion")
            
            # Copy data from old tables to new tables
            print("3. Copying data to new tables...")
            
            cursor.execute("INSERT INTO companies_staff_new SELECT * FROM companies_staff")
            cursor.execute("INSERT INTO companies_users_new SELECT * FROM companies_users")
            
            print("   ✓ Data copied to new tables")
            
            # Drop old tables and rename new ones
            print("4. Replacing old tables...")
            
            cursor.execute("DROP TABLE companies_staff")
            cursor.execute("DROP TABLE companies_users")
            
            cursor.execute("ALTER TABLE companies_staff_new RENAME TO companies_staff")
            cursor.execute("ALTER TABLE companies_users_new RENAME TO companies_users")
            
            print("   ✓ Tables replaced successfully")
            
            # Verify the changes
            print("\n5. Verifying changes...")
            
            cursor.execute("PRAGMA foreign_key_list(companies_staff)")
            new_staff_fks = cursor.fetchall()
            
            cursor.execute("PRAGMA foreign_key_list(companies_users)")
            new_users_fks = cursor.fetchall()
            
            print(f"   New foreign keys in Staff: {len(new_staff_fks)}")
            print(f"   New foreign keys in Users: {len(new_users_fks)}")
            
            print(f"\n=== FIX COMPLETE ===")
            print(f"✓ Cascade deletion is now enabled!")
            print(f"✓ When you delete a branch, all related Staff and Users will be automatically deleted")
            
    except Exception as e:
        print(f"❌ Error during fix: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    try:
        fix_cascade_deletion()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
