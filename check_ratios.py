import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT company_id, year, revenue_cagr_5yr FROM financial_ratios LIMIT 20",
    conn
)

print(df)

conn.close()