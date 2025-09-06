import sqlite3
import re

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Fixing corrupted user_id data ===")

# Get all records with user_id
cursor.execute("SELECT id, user_id FROM companies_users WHERE user_id IS NOT NULL")
all_records = cursor.fetchall()

# Find corrupted records (where user_id is not a number)
corrupted = []
for record in all_records:
    user_id = record[1]
    if not isinstance(user_id, int) and not (isinstance(user_id, str) and user_id.isdigit()):
        corrupted.append(record)

if not corrupted:
    print("No corrupted data found!")
else:
    print(f"Found {len(corrupted)} corrupted records:")
    for record in corrupted:
        print(f"  ID: {record[0]}, user_id: '{record[1]}'")
    
    # Fix the data by setting user_id to NULL for corrupted records
    for record in corrupted:
        cursor.execute("UPDATE companies_users SET user_id = NULL WHERE id = ?", (record[0],))
    
    print(f"Fixed {len(corrupted)} records")
    
    # Verify fix
    cursor.execute("SELECT id, user_id FROM companies_users WHERE user_id IS NOT NULL")
    remaining_records = cursor.fetchall()
    
    still_corrupted = []
    for record in remaining_records:
        user_id = record[1]
        if not isinstance(user_id, int) and not (isinstance(user_id, str) and user_id.isdigit()):
            still_corrupted.append(record)
    
    print(f"Remaining corrupted: {len(still_corrupted)}")
    
    if len(still_corrupted) == 0:
        print("✅ All corrupted data fixed successfully!")
    else:
        print("❌ Some corrupted data remains:")
        for record in still_corrupted:
            print(f"  ID: {record[0]}, user_id: '{record[1]}'")

# Commit and close
conn.commit()
conn.close()

print("\nDatabase fix completed. Now you can run: python manage.py migrate")
