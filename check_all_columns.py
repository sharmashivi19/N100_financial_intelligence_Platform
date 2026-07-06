import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

tables = [
    "companies",
    "financials",
    "balance_sheet",
    "cash_flow",
    "financial_ratios"
]

for table in tables:

    print("\n", table.upper())

    df = pd.read_sql(
        f"SELECT * FROM {table} LIMIT 2",
        conn
    )

    print(df.columns.tolist())

conn.close()