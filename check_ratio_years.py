import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT DISTINCT year FROM financial_ratios",
    conn
)

print(df)

conn.close()