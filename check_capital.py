import pandas as pd

df = pd.read_csv("output/capital_allocation.csv")

print("Companies:", df["company_id"].nunique())

print()

print("Company IDs:")

print(sorted(df["company_id"].unique()))

print()

print("Years:")

print(sorted(df["year"].unique()))