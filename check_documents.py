import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql("SELECT * FROM documents LIMIT 5", conn)

print(df.columns.tolist())
print(df.head())

conn.close()