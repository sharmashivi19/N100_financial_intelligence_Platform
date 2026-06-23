import sqlite3
import csv
import os


conn = sqlite3.connect(
    "database/nifty100.db"
)

tables = [
    "companies",
    "financials",
    "balance_sheet",
    "cash_flow",
    "stock_prices",
    "ratios",
    "market_cap",
    "sector",
    "documents",
    "peer_groups"
]


os.makedirs("data", exist_ok=True)


with open(
    "data/load_audit.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow(
        [
            "table_name",
            "row_count",
            "status"
        ]
    )


    for table in tables:

        count = conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]


        writer.writerow(
            [
                table,
                count,
                "SUCCESS"
            ]
        )


        print(
            table,
            count
        )


conn.close()