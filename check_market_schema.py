import sqlite3

conn = sqlite3.connect("database/nifty100.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(market_cap)")

print(cursor.fetchall())

conn.close()