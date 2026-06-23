import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


years = cursor.execute(
    """
    SELECT DISTINCT year
    FROM financials
    """
).fetchall()


print("Available years:")

for y in years:
    print(y)


conn.close()