#!/usr/bin/env python
"""
Fix all database column mismatches for SML87 project
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.db import connection

def fix_all_columns():
    """Fix all column mismatches in the database"""
    print("🔧 Fixing All Database Column Mismatches")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        try:
            # Check current companies_users table structure
            cursor.execute("PRAGMA table_info(companies_users)")
            current_columns = [col[1] for col in cursor.fetchall()]
            print(f"Current columns: {current_columns}")
            
            # Define the exact columns that Django models expect
            expected_columns = {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'user_id': 'INTEGER',
                'staff_id': 'INTEGER', 
                'full_name': 'VARCHAR(255)',
                'branch': 'INTEGER',  # Django model expects 'branch', not 'branch_id'
                'department': 'VARCHAR(100)',
                'mobile': 'VARCHAR(20)',
                'is_reports': 'BOOLEAN DEFAULT 1',
                'password': 'VARCHAR(128)',
                'status': 'VARCHAR(20) DEFAULT "active"',
                'created_at': 'DATETIME',
                'updated_at': 'DATETIME',
                'extra_data': 'TEXT',
                'raw_csv_data': 'TEXT'
            }
            
            # Add missing columns
            for col_name, col_type in expected_columns.items():
                if col_name not in current_columns:
                    print(f"Adding column: {col_name}")
                    cursor.execute(f"ALTER TABLE companies_users ADD COLUMN {col_name} {col_type}")
                    print(f"✅ Added {col_name}")
                else:
                    print(f"✅ Column {col_name} already exists")
            
            # Rename branch_id to branch if it exists
            if 'branch_id' in current_columns and 'branch' not in current_columns:
                print("Renaming branch_id to branch...")
                # SQLite doesn't support RENAME COLUMN, so we need to recreate the table
                # For now, let's just add the branch column and copy data
                cursor.execute("UPDATE companies_users SET branch = branch_id WHERE branch IS NULL AND branch_id IS NOT NULL")
                print("✅ Data copied from branch_id to branch")
            
            # Map old data to new structure
            if 'user_name' in current_columns:
                print("Mapping old user_name to new full_name...")
                cursor.execute("UPDATE companies_users SET full_name = user_name WHERE full_name IS NULL AND user_name IS NOT NULL")
                print("✅ Data mapped")
            
            # Check if we need to create a proper companies_users table
            print("\n=== Creating Proper Table Structure ===")
            
            # Create a new table with the correct structure
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies_users_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    staff_id INTEGER,
                    full_name VARCHAR(255),
                    branch INTEGER,
                    department VARCHAR(100),
                    mobile VARCHAR(20),
                    is_reports BOOLEAN DEFAULT 1,
                    password VARCHAR(128),
                    status VARCHAR(20) DEFAULT 'active',
                    created_at DATETIME,
                    updated_at DATETIME,
                    extra_data TEXT,
                    raw_csv_data TEXT
                )
            """)
            print("✅ New table structure created")
            
            # Copy data from old table to new table
            print("Copying data to new table...")
            cursor.execute("""
                INSERT INTO companies_users_new (
                    id, user_id, staff_id, full_name, branch, department, 
                    mobile, is_reports, password, status, extra_data, raw_csv_data
                )
                SELECT 
                    id, user_id, staff_id, full_name, branch, department,
                    mobile, is_reports, password, status, extra_data, raw_csv_data
                FROM companies_users
            """)
            print("✅ Data copied to new table")
            
            # Drop old table and rename new table
            print("Replacing old table...")
            cursor.execute("DROP TABLE companies_users")
            cursor.execute("ALTER TABLE companies_users_new RENAME TO companies_users")
            print("✅ Table replaced")
            
            # Create indexes
            print("\n=== Creating Indexes ===")
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_users_user_id ON companies_users(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_users_staff_id ON companies_users(staff_id)",
                "CREATE INDEX IF NOT EXISTS idx_users_branch ON companies_users(branch)",
                "CREATE INDEX IF NOT EXISTS idx_users_full_name ON companies_users(full_name)"
            ]
            
            for index_sql in indexes:
                try:
                    cursor.execute(index_sql)
                    print("✅ Index created")
                except Exception as e:
                    print(f"ℹ️ Index already exists or error: {e}")
            
            # Verify the fix
            print("\n=== Verifying Fix ===")
            cursor.execute("PRAGMA table_info(companies_users)")
            final_columns = [col[1] for col in cursor.fetchall()]
            print(f"Final columns: {final_columns}")
            
            # Check if all expected columns exist
            missing_columns = [col for col in expected_columns.keys() if col not in final_columns]
            if missing_columns:
                print(f"❌ Still missing columns: {missing_columns}")
                return False
            else:
                print("✅ All expected columns are present")
            
            return True
            
        except Exception as e:
            print(f"❌ Error fixing columns: {e}")
            return False

def verify_models():
    """Verify that Django models can now work"""
    print("\n=== Verifying Django Models ===")
    
    try:
        from companies.models import Users, UserPermission, Staff, Branch
        
        # Try to query the models
        user_count = Users.objects.count()
        print(f"✅ Users model working: {user_count} records")
        
        # Try to access key fields
        if Users.objects.exists():
            first_user = Users.objects.first()
            user_id_value = getattr(first_user, 'user_id', None)
            staff_value = getattr(first_user, 'staff', None)
            branch_value = getattr(first_user, 'branch', None)
            print(f"✅ user_id field accessible: {user_id_value}")
            print(f"✅ staff field accessible: {staff_value}")
            print(f"✅ branch field accessible: {branch_value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model verification failed: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 SML87 Complete Database Column Fix")
    print("=" * 60)
    
    # Step 1: Fix all columns
    if not fix_all_columns():
        print("❌ Failed to fix columns")
        return False
    
    # Step 2: Verify models work
    if not verify_models():
        print("❌ Model verification failed")
        return False
    
    print("\n🎉 All database column mismatches fixed!")
    print("The Django server should now work without errors.")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

