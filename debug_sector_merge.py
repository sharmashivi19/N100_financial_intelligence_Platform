import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

sector = pd.read_sql("SELECT * FROM sector", conn)
financials = pd.read_sql("SELECT * FROM financials", conn)
ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
market = pd.read_sql("SELECT * FROM market_cap", conn)

conn.close()

print("=" * 50)
print("TOTAL ROWS")
print("=" * 50)

print("Sector:", len(sector))
print("Financials:", len(financials))
print("Ratios:", len(ratios))
print("Market:", len(market))

print()

print("=" * 50)
print("UNIQUE COMPANIES")
print("=" * 50)

print("Sector:", sector["company_id"].nunique())
print("Financials:", financials["company_id"].nunique())
print("Ratios:", ratios["company_id"].nunique())
print("Market:", market["company_id"].nunique())

print()

sector_ids = set(sector["company_id"])
financial_ids = set(financials["company_id"])
ratio_ids = set(ratios["company_id"])
market_ids = set(market["company_id"])

print("=" * 50)
print("MATCHES")
print("=" * 50)

print("Sector ∩ Financials =", len(sector_ids & financial_ids))
print("Sector ∩ Ratios     =", len(sector_ids & ratio_ids))
print("Sector ∩ Market     =", len(sector_ids & market_ids))

print()

print("=" * 50)
print("MISSING FROM MARKET")
print("=" * 50)

missing = sorted(list(sector_ids - market_ids))

print("Missing:", len(missing))
print(missing[:30])