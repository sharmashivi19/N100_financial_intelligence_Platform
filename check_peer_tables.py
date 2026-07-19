import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("PEER_GROUPS")
peer = pd.read_sql("SELECT * FROM peer_groups LIMIT 5", conn)
print(peer.columns.tolist())
print(peer)

print("\n")

print("PEER_PERCENTILES")
percent = pd.read_sql("SELECT * FROM peer_percentiles LIMIT 5", conn)
print(percent.columns.tolist())
print(percent)

conn.close()