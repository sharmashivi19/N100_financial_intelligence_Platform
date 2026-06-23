import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)


conn.execute(
    "PRAGMA foreign_keys = ON"
)


tables = [
    "financials",
    "balance_sheet",
    "cash_flow",
    "stock_prices"
]


for table in tables:

    result = conn.execute(
        f"PRAGMA foreign_key_check({table})"
    ).fetchall()


    if len(result) == 0:
        print(
            table,
            "FK OK"
        )

    else:
        print(
            table,
            "FAILED",
            result
        )


conn.close()