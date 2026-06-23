import sqlite3

conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()

cursor.execute(
    "SELECT id FROM companies LIMIT 10"
)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()