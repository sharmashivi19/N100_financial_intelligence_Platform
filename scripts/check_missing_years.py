import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)


cursor = conn.cursor()


companies = cursor.execute(
    """
    SELECT DISTINCT company_id
    FROM financials
    """
).fetchall()


for company in companies:

    years = cursor.execute(
        """
        SELECT year
        FROM financials
        WHERE company_id=?
        ORDER BY year
        """,
        (company[0],)
    ).fetchall()


    if len(years) < 5:

        print(
            company[0],
            "has only",
            len(years),
            "years"
        )


conn.close()