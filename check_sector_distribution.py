import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT broad_sector, COUNT(*) as companies FROM sector GROUP BY broad_sector",
    conn
)

print(df)

conn.close()