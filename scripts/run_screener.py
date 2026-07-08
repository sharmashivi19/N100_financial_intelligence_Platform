import sqlite3
import pandas as pd

from src.screener.engine import apply_filters

conn = sqlite3.connect(
    "database/nifty100.db"
)

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

filtered = apply_filters(df)

print(filtered.head())

print()

print("Companies found:", len(filtered))

conn.close()