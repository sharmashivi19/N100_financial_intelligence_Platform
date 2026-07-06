import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT *
FROM financial_ratios
WHERE
return_on_equity_pct > 15
AND debt_to_equity < 1
"""

df = pd.read_sql(query, conn)

print(df)

print("\nTotal Companies:", len(df))

conn.close()