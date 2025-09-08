#!/usr/bin/env python
"""
Comprehensive database fix script for SML87 project
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def check_database_schema():
    """Check the current database schema"""
    print("=== Checking Database Schema ===")
    
    with connection.cursor() as cursor:
        try:
            # Check companies_users table structure
            cursor.execute("PRAGMA table_info(companies_users)")
            columns = cursor.fetchall()
            
            print("Companies_users table columns:")
            for col in columns:
                print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
            
            # Check if user_id column exists
            user_id_exists = any(col[1] == 'user_id' for col in columns)
            user_exists = any(col[1] == 'user' for col in columns)
            
            print(f"\nuser_id column exists: {user_id_exists}")
            print(f"user column exists: {user_exists}")
            
            return user_id_exists, user_exists
            
        except Exception as e:
            print(f"❌ Error checking schema: {e}")
            return False, False

def fix_users_table():
    """Fix the companies_users table schema"""
    print("\n=== Fixing Users Table ===")
    
    with connection.cursor() as cursor:
        try:
            # Check current state
            user_id_exists, user_exists = check_database_schema()
            
            if not user_id_exists:
                print("Adding user_id column...")
                cursor.execute("""
                    ALTER TABLE companies_users 
                    ADD COLUMN user_id INTEGER
                """)
                print("✅ user_id column added")
            else:
                print("✅ user_id column already exists")
            
            # Check if we need to add foreign key constraint
            if user_id_exists:
                try:
                    cursor.execute("""
                        SELECT sql FROM sqlite_master 
                        WHERE type='table' AND name='companies_users'
                    """)
                    table_sql = cursor.fetchone()[0]
                    
                    if 'FOREIGN KEY' not in table_sql or 'auth_user' not in table_sql:
                        print("Adding foreign key constraint...")
                        # SQLite doesn't support adding foreign keys to existing tables
                        # We'll need to recreate the table or handle this differently
                        print("ℹ️ Foreign key constraint will be handled by Django")
                except Exception as e:
                    print(f"ℹ️ Could not check foreign key: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error fixing users table: {e}")
            return False

def run_migrations():
    """Run Django migrations"""
    print("\n=== Running Django Migrations ===")
    
    try:
        # Check migration status
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate', '--plan'])
        
        # Run migrations
        print("Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Migrations completed")
        return True
        
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def verify_fix():
    """Verify that the fix worked"""
    print("\n=== Verifying Fix ===")
    
    try:
        # Try to import and use the models
        from companies.models import Users, UserPermission
        
        # Check if we can query the models
        user_count = Users.objects.count()
        perm_count = UserPermission.objects.count()
        
        print(f"✅ Users model working: {user_count} records")
        print(f"✅ UserPermission model working: {perm_count} records")
        
        # Try to access user_id field
        if Users.objects.exists():
            first_user = Users.objects.first()
            user_id_value = getattr(first_user, 'user_id', None)
            print(f"✅ user_id field accessible: {user_id_value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 SML87 Database Fix Script")
    print("=" * 50)
    
    # Step 1: Check current schema
    user_id_exists, user_exists = check_database_schema()
    
    # Step 2: Fix users table if needed
    if not user_id_exists:
        if not fix_users_table():
            print("❌ Failed to fix users table")
            return False
    
    # Step 3: Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        return False
    
    # Step 4: Verify fix
    if not verify_fix():
        print("❌ Fix verification failed")
        return False
    
    print("\n🎉 Database fix completed successfully!")
    print("You can now run the Django server.")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

