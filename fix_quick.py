import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("UPDATE companies_users SET user_id = NULL WHERE user_id = 'user'")
print(f"Fixed {cursor.rowcount} records")
conn.commit()
conn.close()
print("Done!")
