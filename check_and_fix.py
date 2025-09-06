import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Checking database content ===")

# Check what's in the user_id column
cursor.execute("SELECT id, user_id, typeof(user_id) FROM companies_users WHERE user_id IS NOT NULL")
records = cursor.fetchall()

print(f"Found {len(records)} records with user_id:")
for record in records:
    print(f"  ID: {record[0]}, user_id: '{record[1]}' (type: {record[2]})")

# Find all non-numeric user_id values
corrupted = []
for record in records:
    user_id = record[1]
    if not str(user_id).isdigit():
        corrupted.append(record)

if corrupted:
    print(f"\nFound {len(corrupted)} corrupted records:")
    for record in corrupted:
        print(f"  ID: {record[0]}, user_id: '{record[1]}'")
    
    # Fix all corrupted records
    for record in corrupted:
        cursor.execute("UPDATE companies_users SET user_id = NULL WHERE id = ?", (record[0],))
    
    print(f"Fixed {len(corrupted)} records")
else:
    print("\nNo corrupted records found")

conn.commit()
conn.close()
print("Done!")
