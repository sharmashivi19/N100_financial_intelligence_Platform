import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


print("DATABASE TABLES")
print("================")


tables = cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """
).fetchall()


for table in tables:
    print(table[0])


print("\nROW COUNTS")
print("================")


for table in tables:

    count = cursor.execute(
        f"SELECT COUNT(*) FROM {table[0]}"
    ).fetchone()

    print(
        table[0],
        "->",
        count[0]
    )


conn.close()