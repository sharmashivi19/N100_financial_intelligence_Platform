import sqlite3
import pandas as pd

from src.screener.engine import apply_filters
from src.screener.exporter import export_screener
from src.screener.composite_score import calculate_composite_score

conn = sqlite3.connect(
    "database/nifty100.db"
)

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

df = calculate_composite_score(df)

results = {
    "All Companies": df.sort_values(
        "composite_score",
        ascending=False
    )
}

export_screener(
    results,
    "output/screener_output.xlsx"
)

print("Export completed.")