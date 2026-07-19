import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

sector = pd.read_sql("SELECT * FROM sector LIMIT 5", conn)

financials = pd.read_sql("SELECT * FROM financials LIMIT 5", conn)

ratios = pd.read_sql("SELECT * FROM financial_ratios LIMIT 5", conn)

market = pd.read_sql("SELECT * FROM market_cap LIMIT 5", conn)

print("Sector")
print(sector)

print("\nFinancials")
print(financials)

print("\nRatios")
print(ratios)

print("\nMarket")
print(market)

conn.close()