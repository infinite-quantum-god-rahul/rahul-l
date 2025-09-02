import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=== Faking problematic migration ===")

# Check current migration history
print("1. Current migration history:")
cursor.execute("SELECT app, name, applied FROM django_migrations WHERE app = 'companies' ORDER BY id")
migrations = cursor.fetchall()
for migration in migrations:
    print(f"  {migration[1]} - Applied: {migration[2]}")

# Check if the problematic migration is already recorded
cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app = 'companies' AND name = '0010_remove_users_is_accounting_remove_users_is_admin_and_more'")
exists = cursor.fetchone()[0]

if exists == 0:
    print("\n2. Adding fake migration record...")
    cursor.execute("""
        INSERT INTO django_migrations (app, name, applied) 
        VALUES ('companies', '0010_remove_users_is_accounting_remove_users_is_admin_and_more', datetime('now'))
    """)
    print("✅ Migration marked as completed")
else:
    print("\n2. Migration already exists in history")

# Verify
print("\n3. Updated migration history:")
cursor.execute("SELECT app, name, applied FROM django_migrations WHERE app = 'companies' ORDER BY id")
migrations = cursor.fetchall()
for migration in migrations:
    print(f"  {migration[1]} - Applied: {migration[2]}")

conn.commit()
conn.close()

print("\n✅ Migration faked successfully!")
print("Now try running: python manage.py migrate")
