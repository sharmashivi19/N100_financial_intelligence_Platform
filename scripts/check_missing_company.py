import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


query = """
SELECT *
FROM financials
WHERE company_id IS NULL;
"""


rows = cursor.execute(query).fetchall()


if rows:
    print("Missing company IDs:")
    for row in rows:
        print(row)

else:
    print("No missing company IDs")


conn.close()