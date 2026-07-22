from pathlib import Path
import sqlite3
import pandas as pd
import shutil

# ----------------------------------------
# Create folders
# ----------------------------------------

Path("reports/tearsheets").mkdir(parents=True, exist_ok=True)
Path("output").mkdir(exist_ok=True)

# ----------------------------------------
# Load companies
# ----------------------------------------

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

skipped = []

# ----------------------------------------
# Generate tearsheets
# ----------------------------------------

for _, row in companies.iterrows():

    ticker = row["id"]

    print(f"Generating {ticker}...")

    years = pd.read_sql(
        f"""
        SELECT COUNT(*) AS cnt
        FROM financials
        WHERE company_id='{ticker}'
        """,
        conn
    )

    # Skip companies with fewer than 3 years
    if years.iloc[0]["cnt"] < 3:
        skipped.append(ticker)
        print(f"Skipped {ticker}")
        continue

    # ------------------------------------------------
    # For now copy the existing sample PDF.
    # Later this will call tearsheet.py dynamically.
    # ------------------------------------------------

    source_pdf = Path("output/TCS_Tearsheet.pdf")
    target_pdf = Path(f"reports/tearsheets/{ticker}_tearsheet.pdf")

    if source_pdf.exists():
        shutil.copy(source_pdf, target_pdf)

conn.close()

# ----------------------------------------
# Save skipped companies
# ----------------------------------------

pd.DataFrame(
    {"company_id": skipped}
).to_csv(
    "output/skipped_tearsheets.csv",
    index=False
)

print("=" * 50)
print("Batch Generation Complete")
print("=" * 50)
print("Generated :", len(companies) - len(skipped))
print("Skipped :", len(skipped))