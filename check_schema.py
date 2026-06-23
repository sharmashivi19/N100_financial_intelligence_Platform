import sqlite3

conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()

tables = cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """
).fetchall()

for table in tables:
    print("\nTABLE:", table[0])

    columns = cursor.execute(
        f"PRAGMA table_info({table[0]});"
    ).fetchall()

    for col in columns:
        print(col[1])

conn.close()