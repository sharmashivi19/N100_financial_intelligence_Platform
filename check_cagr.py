import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT revenue_cagr_5yr FROM financial_ratios",
    conn
)

print(df["revenue_cagr_5yr"].describe())

print("\nNull values:")
print(df["revenue_cagr_5yr"].isna().sum())

conn.close()