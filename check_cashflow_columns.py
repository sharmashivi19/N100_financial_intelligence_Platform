import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM cash_flow LIMIT 5",
    conn
)

conn.close()

print(df.columns.tolist())
print(df.head())