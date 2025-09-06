import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Resetting companies_users table ===")

# Backup current data (excluding user_id and role fields)
print("1. Backing up current data...")
cursor.execute("""
    SELECT id, extra_data, raw_csv_data, full_name, department, mobile, status, 
           password, staff_id, branch
    FROM companies_users
""")
backup_data = cursor.fetchall()
print(f"Backed up {len(backup_data)} records")

# Drop and recreate the table
print("2. Dropping and recreating table...")
cursor.execute("DROP TABLE companies_users")

# Recreate the table with correct structure (without role fields and user_id)
cursor.execute("""
CREATE TABLE companies_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    extra_data TEXT,
    raw_csv_data TEXT,
    full_name VARCHAR(255),
    department VARCHAR(100),
    mobile VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    password VARCHAR(128),
    staff_id BIGINT,
    branch BIGINT,
    is_reports BOOLEAN NOT NULL DEFAULT 1
)
""")

# Restore data (without role fields and user_id)
print("3. Restoring data...")
for record in backup_data:
    cursor.execute("""
        INSERT INTO companies_users 
        (id, extra_data, raw_csv_data, full_name, department, mobile, status, password, staff_id, branch)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, record)

print(f"Restored {len(backup_data)} records")

# Verify
cursor.execute("SELECT COUNT(*) FROM companies_users")
total = cursor.fetchone()[0]
print(f"Total records in table: {total}")

# Show new structure
print("\n4. New table structure:")
cursor.execute("PRAGMA table_info(companies_users)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]} ({col[2]}) - nullable: {not col[3]}")

conn.commit()
conn.close()

print("\n✅ Table reset completed!")
print("Now try running: python manage.py migrate")
