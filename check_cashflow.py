import pandas as pd

df = pd.read_excel(
    "data/source_files/cash_flow.xlsx",
    header=1
)

print(df.columns.tolist())
print(df.head())