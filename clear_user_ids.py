import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Clearing all user_id values temporarily ===")

# Backup current values
cursor.execute("SELECT id, user_id FROM companies_users WHERE user_id IS NOT NULL")
backup = cursor.fetchall()
print(f"Backing up {len(backup)} user_id values:")
for record in backup:
    print(f"  ID: {record[0]}, user_id: {record[1]}")

# Clear all user_id values
cursor.execute("UPDATE companies_users SET user_id = NULL")
print(f"Cleared {cursor.rowcount} user_id values")

# Verify clear
cursor.execute("SELECT COUNT(*) FROM companies_users WHERE user_id IS NOT NULL")
remaining = cursor.fetchone()[0]
print(f"Remaining user_id values: {remaining}")

conn.commit()
conn.close()

print("\n✅ All user_id values cleared temporarily!")
print("Now try running: python manage.py migrate")
print("After migration succeeds, you can restore the user_id values if needed.")
