#!/usr/bin/env python
"""
Database Column Fix Script
Fixes missing columns in database tables
"""
import sqlite3
import os

def fix_database():
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Fixing database columns...")
        
        # Fix companies_users table
        try:
            cursor.execute("ALTER TABLE companies_users ADD COLUMN user_id INTEGER")
            print("✅ Added user_id column to companies_users")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✅ user_id column already exists in companies_users")
            else:
                print(f"⚠️ Could not add user_id to companies_users: {e}")
        
        # Fix companies_role table
        try:
            cursor.execute("ALTER TABLE companies_role ADD COLUMN description TEXT")
            print("✅ Added description column to companies_role")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✅ description column already exists in companies_role")
            else:
                print(f"⚠️ Could not add description to companies_role: {e}")
        
        try:
            cursor.execute("ALTER TABLE companies_role ADD COLUMN permissions TEXT")
            print("✅ Added permissions column to companies_role")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✅ permissions column already exists in companies_role")
            else:
                print(f"⚠️ Could not add permissions to companies_role: {e}")
        
        try:
            cursor.execute("ALTER TABLE companies_role ADD COLUMN is_active BOOLEAN DEFAULT 1")
            print("✅ Added is_active column to companies_role")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✅ is_active column already exists in companies_role")
            else:
                print(f"⚠️ Could not add is_active to companies_role: {e}")
        
        # Fix companies_client table
        try:
            cursor.execute("ALTER TABLE companies_client ADD COLUMN GCode VARCHAR(255)")
            print("✅ Added GCode column to companies_client")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("✅ GCode column already exists in companies_client")
            else:
                print(f"⚠️ Could not add GCode to companies_client: {e}")
        
        conn.commit()
        conn.close()
        print("🎉 Database fix completed successfully!")
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")

if __name__ == "__main__":
    fix_database()

