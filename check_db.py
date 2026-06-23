import sqlite3

conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()

cursor.execute(
    "PRAGMA table_info(financials)"
)

for row in cursor.fetchall():
    print(row)

conn.close()