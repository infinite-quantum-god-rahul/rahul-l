import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Checking auth_user table ===")
cursor.execute("SELECT id, username, email FROM auth_user")
auth_users = cursor.fetchall()
print(f"Found {len(auth_users)} users in auth_user:")
for user in auth_users:
    print(f"  ID: {user[0]}, username: {user[1]}, email: {user[2]}")

print("\n=== Checking companies_users table ===")
cursor.execute("SELECT id, user_id, full_name FROM companies_users WHERE user_id IS NOT NULL")
comp_users = cursor.fetchall()
print(f"Found {len(comp_users)} users in companies_users:")
for user in comp_users:
    print(f"  ID: {user[0]}, user_id: {user[1]}, full_name: {user[2]}")

print("\n=== Checking for mismatches ===")
# Find companies_users records where user_id doesn't exist in auth_user
cursor.execute("""
    SELECT c.id, c.user_id, c.full_name 
    FROM companies_users c 
    LEFT JOIN auth_user a ON c.user_id = a.id 
    WHERE c.user_id IS NOT NULL AND a.id IS NULL
""")
mismatches = cursor.fetchall()

if mismatches:
    print(f"Found {len(mismatches)} mismatched records:")
    for record in mismatches:
        print(f"  ID: {record[0]}, user_id: {record[1]}, full_name: {record[2]}")
    
    # Fix mismatches by setting user_id to NULL
    for record in mismatches:
        cursor.execute("UPDATE companies_users SET user_id = NULL WHERE id = ?", (record[0],))
    
    print(f"Fixed {len(mismatches)} mismatched records")
else:
    print("No mismatches found")

conn.commit()
conn.close()
print("Done!")
