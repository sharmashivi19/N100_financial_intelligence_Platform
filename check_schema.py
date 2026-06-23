import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


cursor.execute(
    "PRAGMA table_info(companies)"
)


columns = cursor.fetchall()


for col in columns:
    print(col)


conn.close()