import sqlite3
import pandas as pd

from src.screener.composite_score import (
    calculate_composite_score
)

conn = sqlite3.connect(
    "database/nifty100.db"
)

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

df = calculate_composite_score(df)

print(
    df[
        [
            "company_id",
            "composite_score"
        ]
    ].head()
)