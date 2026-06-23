import sqlite3
import random


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


# Get 5 random companies

companies = cursor.execute(
    """
    SELECT id, company_name
    FROM companies
    ORDER BY RANDOM()
    LIMIT 5
    """
).fetchall()


print("\nRandom 5 Companies\n")


for company in companies:

    company_id = company[0]
    name = company[1]

    print("--------------------")
    print("Company:", name)
    print("ID:", company_id)


    years = cursor.execute(
        """
        SELECT DISTINCT year
        FROM financials
        WHERE company_id=?
        ORDER BY year
        """,
        (company_id,)
    ).fetchall()


    print(
        "Financial Years:",
        len(years)
    )

    print(
        years
    )


conn.close()