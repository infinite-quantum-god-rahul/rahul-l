import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Current database state ===")

# Check companies_users table structure
print("\n1. Companies_users table structure:")
cursor.execute("PRAGMA table_info(companies_users)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]} ({col[2]}) - nullable: {not col[3]}")

# Check all data in companies_users
print("\n2. All data in companies_users:")
cursor.execute("SELECT * FROM companies_users")
records = cursor.fetchall()
for record in records:
    print(f"  Record: {record}")

# Check if there are any hidden columns or data
print("\n3. Checking for hidden data:")
cursor.execute("SELECT COUNT(*) FROM companies_users")
total = cursor.fetchone()[0]
print(f"  Total records: {total}")

cursor.execute("SELECT id, user_id, typeof(user_id) FROM companies_users")
all_data = cursor.fetchall()
for record in all_data:
    print(f"  ID: {record[0]}, user_id: '{record[1]}' (type: {record[2]})")

# Check if there are any constraints
print("\n4. Table constraints:")
cursor.execute("PRAGMA foreign_key_list(companies_users)")
constraints = cursor.fetchall()
for constraint in constraints:
    print(f"  Foreign key: {constraint}")

conn.close()
print("\nDone!")
