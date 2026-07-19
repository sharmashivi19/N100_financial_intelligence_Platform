import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM analysis LIMIT 5",
    conn
)

print(df.columns.tolist())
print(df.head())

conn.close()