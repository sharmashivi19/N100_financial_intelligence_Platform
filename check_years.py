import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

financials = pd.read_sql(
    "SELECT DISTINCT year FROM financials ORDER BY year DESC LIMIT 10",
    conn
)

market = pd.read_sql(
    "SELECT DISTINCT year FROM market_cap ORDER BY year DESC LIMIT 10",
    conn
)

ratios = pd.read_sql(
    "SELECT DISTINCT year FROM financial_ratios ORDER BY year DESC LIMIT 10",
    conn
)

print("Financials years:")
print(financials)

print("\nMarket Cap years:")
print(market)

print("\nRatios years:")
print(ratios)

conn.close()