import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Adding user field to companies_users table ===")

# Check current structure
print("1. Current table structure:")
cursor.execute("PRAGMA table_info(companies_users)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]} ({col[2]}) - nullable: {not col[3]}")

# Add user_id field
print("\n2. Adding user_id field...")
try:
    cursor.execute("ALTER TABLE companies_users ADD COLUMN user_id INTEGER")
    print("✅ user_id field added successfully")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️ user_id field already exists")
    else:
        print(f"❌ Error adding user_id field: {e}")

# Verify new structure
print("\n3. Updated table structure:")
cursor.execute("PRAGMA table_info(companies_users)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]} ({col[2]}) - nullable: {not col[3]}")

conn.commit()
conn.close()

print("\n✅ Table structure updated!")
print("Now try accessing your website again")
