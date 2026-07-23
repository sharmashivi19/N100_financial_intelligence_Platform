from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
styles = getSampleStyleSheet()

title = styles["Heading1"]
heading = styles["Heading2"]
normal = styles["BodyText"]
from pathlib import Path

Path("reports/portfolio").mkdir(
    parents=True,
    exist_ok=True
)
import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/nifty100.db"
)
companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

sector = pd.read_sql(
    "SELECT * FROM sector",
    conn
)

financials = pd.read_sql(
    "SELECT * FROM financials",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()
financials = (
    financials
    .groupby("company_id", as_index=False)
    .last()
)

ratios = (
    ratios
    .groupby("company_id", as_index=False)
    .last()
)
financials = (
    financials
    .groupby("company_id", as_index=False)
    .last()
)

ratios = (
    ratios
    .groupby("company_id", as_index=False)
    .last()
)
# -----------------------------------------
# Merge all tables
# -----------------------------------------

df = companies.rename(
    columns={"id": "company_id"}
)

df = df.merge(
    sector,
    on="company_id",
    how="left"
)

df = df.merge(
    financials,
    on="company_id",
    how="left"
)

df = df.merge(
    ratios,
    on="company_id",
    how="left"
)

df = df.sort_values("company_id")
pdf = SimpleDocTemplate(
    "reports/portfolio/portfolio_summary.pdf"
)

story = []
for _, row in df.iterrows():

    story.append(
        Paragraph(
            f"<b>{row['company_name']}</b>",
            title
        )
    )

    story.append(
        Paragraph(
            f"Ticker : {row['company_id']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"Sector : {row['broad_sector']}",
            normal
        )
    )

    story.append(PageBreak())
pdf.build(story)

print("=" * 50)
print("Portfolio Summary Generated")
print("=" * 50)
print("Saved to reports/portfolio/portfolio_summary.pdf")