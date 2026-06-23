import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)


cursor = conn.cursor()


result = cursor.execute(
    """
    SELECT 
        company_id,
        COUNT(DISTINCT year) AS year_count
    FROM financials
    GROUP BY company_id
    HAVING year_count < 5
    """
).fetchall()



print(
    "Companies with less than 5 years:"
)


for row in result:
    print(row)


print(
    "Total:",
    len(result)
)


conn.close()