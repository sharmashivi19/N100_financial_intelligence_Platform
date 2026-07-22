import sqlite3
from pathlib import Path
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

# -------------------------------------------------------
# Output Folder
# -------------------------------------------------------

Path("reports/sector").mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# Database
# -------------------------------------------------------

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)
sector = pd.read_sql("SELECT * FROM sector", conn)

financials = pd.read_sql("""
SELECT
company_id,
sales,
operating_profit,
net_profit,
eps,
dividend_payout
FROM financials
""", conn)

ratios = pd.read_sql("""
SELECT
company_id,
return_on_equity_pct,
debt_to_equity,
interest_coverage,
asset_turnover
FROM financial_ratios
""", conn)

conn.close()

# -------------------------------------------------------
# Latest Financials
# -------------------------------------------------------

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

# -------------------------------------------------------
# Merge
# -------------------------------------------------------

df = companies.rename(columns={"id": "company_id"})

df = df.merge(sector, on="company_id", how="left")
df = df.merge(financials, on="company_id", how="left")
df = df.merge(ratios, on="company_id", how="left")

# -------------------------------------------------------
# Styles
# -------------------------------------------------------

styles = getSampleStyleSheet()
title = styles["Heading1"]
heading = styles["Heading2"]

# -------------------------------------------------------
# Sector List
# -------------------------------------------------------

sector_list = sorted(df["broad_sector"].dropna().unique())

print("Sectors Found:")
print(sector_list)

# -------------------------------------------------------
# Generate Reports
# -------------------------------------------------------

for sec in sector_list:

    sector_df = df[df["broad_sector"] == sec].copy()

    pdf = SimpleDocTemplate(
        f"reports/sector/{sec}_report.pdf",
        pagesize=(8.27 * inch, 11.69 * inch)
    )

    story = []

    # ---------------------------------------------------

    story.append(
        Paragraph(f"{sec} Sector Report", title)
    )

    story.append(Spacer(1, 20))

    # ---------------------------------------------------
    # Sector Summary
    # ---------------------------------------------------

    summary = [

        ["Metric", "Median"],

        ["Revenue",
         round(sector_df["sales"].median(),2)],

        ["Operating Profit",
         round(sector_df["operating_profit"].median(),2)],

        ["Net Profit",
         round(sector_df["net_profit"].median(),2)],

        ["ROE %",
         round(sector_df["return_on_equity_pct"].median(),2)],

        ["Debt / Equity",
         round(sector_df["debt_to_equity"].median(),2)],

        ["Interest Coverage",
         round(sector_df["interest_coverage"].median(),2)],

        ["Asset Turnover",
         round(sector_df["asset_turnover"].median(),2)],

        ["EPS",
         round(sector_df["eps"].median(),2)]

    ]

    table = Table(summary, colWidths=[3*inch,2*inch])

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("ALIGN",(1,1),(-1,-1),"CENTER"),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

    ]))

    story.append(table)

    story.append(Spacer(1,20))

    # ---------------------------------------------------
    # Company Table
    # ---------------------------------------------------

    story.append(
        Paragraph("Companies", heading)
    )

    story.append(Spacer(1,10))

    table_data = [[

        "Company",

        "Sales",

        "PAT",

        "ROE",

        "D/E",

        "Interest",

        "Asset Turn",

        "EPS"

    ]]

    for _, row in sector_df.iterrows():

        table_data.append([

            row["company_name"],

            row["sales"],

            row["net_profit"],

            row["return_on_equity_pct"],

            row["debt_to_equity"],

            row["interest_coverage"],

            row["asset_turnover"],

            row["eps"]

        ])

    company_table = Table(

        table_data,

        repeatRows=1,

        colWidths=[
            2.2*inch,
            0.8*inch,
            0.8*inch,
            0.7*inch,
            0.7*inch,
            0.8*inch,
            0.8*inch,
            0.7*inch
        ]

    )

    company_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.navy),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.25,colors.grey),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,0),6)

    ]))

    story.append(company_table)

    pdf.build(story)

    print(f"Created -> {sec}_report.pdf")

print("="*50)
print("All Sector Reports Generated Successfully")
print("="*50)