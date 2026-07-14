import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

print("Columns:")
print(companies.columns.tolist())

print("\nFirst 5 rows:")
print(companies.head())

conn.close()