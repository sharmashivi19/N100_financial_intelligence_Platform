import sqlite3
import pandas as pd
import yaml
import os

from src.screener.engine import apply_filters

PRESET = "turnaround_watch"

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

with open("config/presets.yaml") as f:
    presets = yaml.safe_load(f)

config = presets[PRESET]

result = apply_filters(df, config)

print(result.head())

print()

print("Companies found:", len(result))

os.makedirs("output", exist_ok=True)

result.to_excel(
    f"output/{PRESET}.xlsx",
    index=False
)

print(f"{PRESET}.xlsx generated!")