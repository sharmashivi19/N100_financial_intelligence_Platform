import sqlite3
import pandas as pd

db = "database/nifty100.db"
excel = "data/source_files/peer_groups.xlsx"

conn = sqlite3.connect(db)

# Load correct Excel
df = pd.read_excel(excel)

# Replace table
df.to_sql(
    "peer_groups",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("✅ peer_groups repaired successfully")