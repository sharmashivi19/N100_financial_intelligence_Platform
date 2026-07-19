import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT DISTINCT year FROM financials",
    conn
)

print(df)

conn.close()