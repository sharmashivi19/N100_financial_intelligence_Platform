from src.ingestion.loader import load_excel
import pandas as pd


files = [

    (
        "data/source_files/companies.xlsx",
        "companies"
    ),

    (
        "data/source_files/pnl.xlsx",
        "financials"
    ),

    (
        "data/source_files/balance_sheet.xlsx",
        "balance_sheet"
    ),

    (
        "data/source_files/cash_flow.xlsx",
        "cash_flow"
    ),

    (
        "data/source_files/prices.xlsx",
        "stock_prices"
    ),

    (
        "data/source_files/ratios.xlsx",
        "ratios"
    ),

    (
        "data/source_files/market_cap.xlsx",
        "market_cap"
    ),

    (
        "data/source_files/sector.xlsx",
        "sector"
    ),

    (
        "data/source_files/documents.xlsx",
        "documents"
    ),

    (
        "data/source_files/peer_groups.xlsx",
        "peer_groups"
    )

]


audit = []


for file, table in files:

    print("Processing:", file)

    count = load_excel(
        file,
        table
    )


    audit.append(
        {
            "file": file,
            "table": table,
            "rows_loaded": count
        }
    )


df = pd.DataFrame(audit)


df.to_csv(
    "data/load_audit.csv",
    index=False
)


print("Full data load completed")