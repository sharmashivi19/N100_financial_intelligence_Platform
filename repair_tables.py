import sqlite3
import pandas as pd

DB = "database/nifty100.db"

conn = sqlite3.connect(DB)

# -----------------------------
# Fix sector table
# -----------------------------
sector = pd.read_excel("data/source_files/sector.xlsx")

conn.execute("DROP TABLE IF EXISTS sector")

sector.to_sql(
    "sector",
    conn,
    index=False,
    if_exists="replace"
)

print("✓ sector table repaired")

# -----------------------------
# Fix market_cap table
# -----------------------------
market = pd.read_excel("data/source_files/market_cap.xlsx")

conn.execute("DROP TABLE IF EXISTS market_cap")

market.to_sql(
    "market_cap",
    conn,
    index=False,
    if_exists="replace"
)

print("✓ market_cap table repaired")

conn.close()

print("\nDatabase repaired successfully!")