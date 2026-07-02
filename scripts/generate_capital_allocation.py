import pandas as pd

from src.analytics.cashflow import (
    sign,
    capital_allocation_pattern,
)

# Read Excel using the correct header row
df = pd.read_excel(
    "data/source_files/cash_flow.xlsx",
    header=1
)

# Create sign columns
df["cfo_sign"] = df["operating_activity"].apply(sign)
df["cfi_sign"] = df["investing_activity"].apply(sign)
df["cff_sign"] = df["financing_activity"].apply(sign)

# Create pattern labels
df["pattern_label"] = df.apply(
    lambda row: capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
    ),
    axis=1,
)

# Select output columns
output = df[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label",
    ]
]

# Save CSV
output.to_csv(
    "output/capital_allocation.csv",
    index=False,
)

print("capital_allocation.csv generated successfully!")