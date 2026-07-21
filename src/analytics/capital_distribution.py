import pandas as pd
from pathlib import Path

Path("output").mkdir(exist_ok=True)

df = pd.read_csv("output/capital_allocation.csv")

# Keep the latest record for every company
latest = (
    df.sort_values("year")
      .groupby("company_id", as_index=False)
      .last()
)

summary = (
    latest.groupby("pattern_label")
    .size()
    .reset_index(name="companies")
)

summary.to_csv(
    "output/capital_distribution_summary.csv",
    index=False
)

print(summary)