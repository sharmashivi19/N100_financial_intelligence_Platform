import pandas as pd

df = pd.read_excel(
    "data/source_files/pnl.xlsx",
    engine="openpyxl",
    header=1
)

print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nCompany IDs:")
print(df["company_id"].head(10))