#!/usr/bin/env python
import sqlite3
import os

def fix_database():
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user_id column exists
        cursor.execute("PRAGMA table_info(companies_users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("Adding user_id column to companies_users table...")
            cursor.execute("ALTER TABLE companies_users ADD COLUMN user_id INTEGER")
            conn.commit()
            print("✅ Added user_id column successfully!")
        else:
            print("✅ user_id column already exists!")
        
        conn.close()
        print("Database fix completed!")
        
    except Exception as e:
        print(f"Error fixing database: {e}")

if __name__ == "__main__":
    fix_database()

