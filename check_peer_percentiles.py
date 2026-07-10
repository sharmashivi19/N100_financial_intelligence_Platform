import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

print(df.head())

print("\nRows:", len(df))

print("\nUnique Peer Groups:")
print(df["peer_group_name"].unique())

conn.close()