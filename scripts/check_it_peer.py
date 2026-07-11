import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql("""
SELECT *
FROM peer_percentiles
WHERE peer_group_name='IT Services'
AND metric='return_on_equity_pct'
ORDER BY percentile_rank DESC
""", conn)

print(df.head(10))

conn.close()