import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("FINANCIALS")
print(pd.read_sql("SELECT * FROM financials LIMIT 2", conn).columns.tolist())

print("\nBALANCE SHEET")
print(pd.read_sql("SELECT * FROM balance_sheet LIMIT 2", conn).columns.tolist())

print("\nCASH FLOW")
print(pd.read_sql("SELECT * FROM cash_flow LIMIT 2", conn).columns.tolist())

conn.close()