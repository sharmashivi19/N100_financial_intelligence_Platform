import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)


tables = [
    "companies",
    "financials",
    "balance_sheet",
    "cash_flow",
    "stock_prices"
]


for table in tables:

    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(
        table,
        "=",
        count
    )


conn.close()