import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


columns = cursor.execute(
    "PRAGMA table_info(sector);"
).fetchall()


for col in columns:
    print(col)


conn.close()