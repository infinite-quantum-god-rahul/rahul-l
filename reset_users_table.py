import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Resetting companies_users table ===")

# Backup current data (excluding user_id)
print("1. Backing up current data...")
cursor.execute("SELECT id, full_name, branch_id, department, mobile, is_reports, status, password, staff_id FROM companies_users")
backup_data = cursor.fetchall()
print(f"Backed up {len(backup_data)} records")

# Drop and recreate the table
print("2. Dropping and recreating table...")
cursor.execute("DROP TABLE companies_users")

# Recreate the table with correct structure
cursor.execute("""
CREATE TABLE companies_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(255),
    branch_id INTEGER,
    department VARCHAR(100),
    mobile VARCHAR(20),
    is_reports BOOLEAN NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    password VARCHAR(128),
    staff_id INTEGER,
    extra_data TEXT,
    raw_csv_data TEXT
)
""")

# Restore data (without user_id)
print("3. Restoring data...")
for record in backup_data:
    cursor.execute("""
        INSERT INTO companies_users 
        (id, full_name, branch_id, department, mobile, is_reports, status, password, staff_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, record)

print(f"Restored {len(backup_data)} records")

# Verify
cursor.execute("SELECT COUNT(*) FROM companies_users")
total = cursor.fetchone()[0]
print(f"Total records in table: {total}")

conn.commit()
conn.close()

print("\n✅ Table reset completed!")
print("Now try running: python manage.py migrate")
