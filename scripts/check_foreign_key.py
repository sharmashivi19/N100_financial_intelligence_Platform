import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


query = """
SELECT financials.company_id
FROM financials
LEFT JOIN companies
ON financials.company_id = companies.id
WHERE companies.id IS NULL;
"""


result = cursor.execute(query).fetchall()


if result:
    print("Invalid company references:")
    for row in result:
        print(row)

else:
    print("All foreign keys are valid")


conn.close()