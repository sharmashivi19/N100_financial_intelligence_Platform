import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


query = """
SELECT 
    company_id,
    year,
    COUNT(*) 
FROM financials
GROUP BY company_id, year
HAVING COUNT(*) > 1;
"""


result = cursor.execute(query).fetchall()


if result:
    print("Duplicate financial records found:")
    for row in result:
        print(row)

else:
    print("No duplicate records found")


conn.close()