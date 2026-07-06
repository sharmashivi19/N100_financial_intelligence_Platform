import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)

print(companies.columns.tolist())

conn.close()