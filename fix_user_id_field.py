#!/usr/bin/env python
"""
Fix the missing user_id field in companies_users table
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.db import connection

def fix_user_id_field():
    """Add the missing user_id field to companies_users table"""
    print("=== Fixing missing user_id field ===")
    
    with connection.cursor() as cursor:
        try:
            # Check if user_id column exists
            cursor.execute("PRAGMA table_info(companies_users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'user_id' not in columns:
                print("Adding user_id column...")
                cursor.execute("""
                    ALTER TABLE companies_users 
                    ADD COLUMN user_id INTEGER REFERENCES auth_user(id)
                """)
                print("✅ user_id column added successfully")
            else:
                print("✅ user_id column already exists")
            
            # Check if user column exists
            if 'user' not in columns:
                print("✅ user column already removed (as expected)")
            else:
                print("ℹ️ user column still exists (will be handled by migration)")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print("\n✅ Database schema fixed!")
    return True

if __name__ == "__main__":
    success = fix_user_id_field()
    if success:
        print("\n🎉 You can now run the Django server!")
    else:
        print("\n❌ Failed to fix database schema")
        sys.exit(1)

