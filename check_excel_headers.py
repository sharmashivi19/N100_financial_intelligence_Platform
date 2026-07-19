import pandas as pd

print("===== sector.xlsx =====")
sector = pd.read_excel("data/source_files/sector.xlsx")
print(sector.columns.tolist())
print(sector.head())

print("\n===== market_cap.xlsx =====")
market = pd.read_excel("data/source_files/market_cap.xlsx")
print(market.columns.tolist())
print(market.head())