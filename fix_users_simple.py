#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.db import connection

def fix_users():
    print("Fixing corrupted user_id data...")
    
    with connection.cursor() as cursor:
        # Find corrupted records
        cursor.execute("SELECT id, user_id FROM companies_users WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL")
        corrupted = cursor.fetchall()
        
        if not corrupted:
            print("No corrupted data found!")
            return
        
        print(f"Found {len(corrupted)} corrupted records:")
        for record in corrupted:
            print(f"  ID: {record[0]}, user_id: '{record[1]}'")
        
        # Fix by setting user_id to NULL
        cursor.execute("UPDATE companies_users SET user_id = NULL WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL")
        print(f"Fixed {cursor.rowcount} records")
        
        # Verify fix
        cursor.execute("SELECT COUNT(*) FROM companies_users WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL")
        remaining = cursor.fetchone()[0]
        print(f"Remaining corrupted: {remaining}")

if __name__ == "__main__":
    fix_users()
