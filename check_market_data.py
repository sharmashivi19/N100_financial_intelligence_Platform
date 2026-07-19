import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM market_cap LIMIT 5",
    conn
)

print("Columns:")
print(df.columns.tolist())

print("\nData:")
print(df)

conn.close()