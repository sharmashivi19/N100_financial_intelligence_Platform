import sqlite3

conn = sqlite3.connect("database/nifty100.db")

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")

print("Total rows:", cursor.fetchone()[0])

conn.close()