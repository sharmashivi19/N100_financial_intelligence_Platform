import sqlite3
import time

from fastapi import APIRouter

router = APIRouter()

START_TIME = time.time()

DATABASE = "database/nifty100.db"


@router.get("/health")
def health():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    tables = [
        "companies",
        "sector",
        "financials",
        "financial_ratios",
        "balance_sheet",
        "cash_flow",
        "shareholding_pattern",
        "pros_cons",
        "quarterly_results",
        "promoter_holdings"
    ]

    row_counts = {}

    for table in tables:

        try:

            cursor.execute(f"SELECT COUNT(*) FROM {table}")

            row_counts[table] = cursor.fetchone()[0]

        except Exception:

            row_counts[table] = "Table Not Found"

    conn.close()

    return {

        "status": "ok",

        "version": "1.0.0",

        "uptime_seconds": round(
            time.time() - START_TIME,
            2
        ),

        "db_row_counts": row_counts

    }