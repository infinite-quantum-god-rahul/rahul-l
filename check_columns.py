import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Checking companies_users table structure ===")

# Get table info
cursor.execute("PRAGMA table_info(companies_users)")
columns = cursor.fetchall()

print("Columns in companies_users table:")
for col in columns:
    print(f"  {col[1]} ({col[2]}) - nullable: {not col[3]}")

# Get sample data
print("\nSample data (first 2 records):")
cursor.execute("SELECT * FROM companies_users LIMIT 2")
records = cursor.fetchall()
for i, record in enumerate(records):
    print(f"  Record {i+1}: {record}")

conn.close()
print("\nDone!")
