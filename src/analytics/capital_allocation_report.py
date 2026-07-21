import pandas as pd
from pathlib import Path

Path("output").mkdir(exist_ok=True)

capital = pd.read_csv("output/capital_allocation.csv")
print("="*50)
print("Capital Allocation Data")
print("="*50)

print(capital.head())

print()

print("Rows :", len(capital))
print("Companies :", capital["company_id"].nunique())
print("Years :", capital["year"].nunique())