import matplotlib.pyplot as plt

from reportlab.platypus import Image
import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

# ----------------------------------------
# Output Folder
# ----------------------------------------

Path("output").mkdir(exist_ok=True)
Path("output/charts").mkdir(parents=True, exist_ok=True)
# ----------------------------------------
# Choose Company
# ----------------------------------------
conn = sqlite3.connect("database/nifty100.db")
COMPANY = "TCS"
company = pd.read_sql(
    f"""
    SELECT *
    FROM companies
    WHERE id='{COMPANY}'
    """,
    conn
)

financials = pd.read_sql(
    f"""
    SELECT *
    FROM financials
    WHERE company_id='{COMPANY}'
    ORDER BY year
    """,
    conn
)
balancesheet = pd.read_sql(
    f"""
    SELECT *
    FROM balance_sheet
    WHERE company_id='{COMPANY}'
    ORDER BY year
    """,
    conn
)

cashflow = pd.read_sql(
    f"""
    SELECT *
    FROM cash_flow
    WHERE company_id='{COMPANY}'
    ORDER BY year
    """,
    conn
)

pros_cons = pd.read_csv(
    "output/pros_cons_generated.csv"
)

capital = pd.read_csv(
    "output/capital_allocation.csv"
)
ratios = pd.read_sql(
    f"""
    SELECT *
    FROM financial_ratios
    WHERE company_id='{COMPANY}'
    ORDER BY year
    """,
    conn
)

conn.close()
# ----------------------------------------
# Revenue Chart
# ----------------------------------------

plt.figure(figsize=(5,3))

plt.bar(
    financials["year"],
    financials["sales"]
)

plt.title("Revenue")

plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig(
    "output/charts/revenue.png"
)

plt.close()
# ----------------------------------------
# Net Profit Chart
# ----------------------------------------

plt.figure(figsize=(5,3))

plt.bar(
    financials["year"],
    financials["net_profit"]
)

plt.title("Net Profit")

plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig(
    "output/charts/netprofit.png"
)

plt.close()
# ----------------------------------------
# ROE Chart
# ----------------------------------------

plt.figure(figsize=(5,3))

plt.plot(
    ratios["year"],
    ratios["return_on_equity_pct"],
    marker="o"
)

plt.title("ROE %")

plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig(
    "output/charts/roe.png"
)

plt.close()
# ----------------------------------------
# ROCE Chart
# ----------------------------------------

plt.figure(figsize=(5,3))

plt.plot(
    ratios["year"],
    [company.iloc[0]["roce_percentage"]]*len(ratios),
    marker="o"
)

plt.title("ROCE %")

plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig(
    "output/charts/roce.png"
)

plt.close()
# ----------------------------------------
# Latest Values
# ----------------------------------------

latest_fin = financials.iloc[-1]
latest_ratio = ratios.iloc[-1]

# ----------------------------------------
# Styles
# ----------------------------------------

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
normal = styles["BodyText"]

import matplotlib.pyplot as plt

Path("output/charts").mkdir(exist_ok=True)

plt.figure(figsize=(6,3))

plt.bar(
    balancesheet["year"],
    balancesheet["equity_capital"],
    label="Equity Capital"
)

plt.bar(
    balancesheet["year"],
    balancesheet["borrowings"],
    bottom=balancesheet["equity_capital"],
    label="Borrowings"
)

plt.bar(
    balancesheet["year"],
    balancesheet["other_liabilities"],
    bottom=
        balancesheet["equity_capital"] +
        balancesheet["borrowings"],
    label="Other Liabilities"
)
plt.xticks(rotation=90)

plt.legend()

plt.tight_layout()

plt.savefig("output/charts/balance_sheet.png")

plt.close()
latest = cashflow.iloc[-1]

labels = [
    "CFO",
    "CFI",
    "CFF",
    "Net Cash"
]

values = [

    latest["operating_activity"],

    latest["investing_activity"],

    latest["financing_activity"],

    latest["net_cash_flow"]

]

plt.figure(figsize=(5,3))

plt.bar(labels, values)

plt.title("Latest Cash Flow")

plt.tight_layout()

plt.savefig("output/charts/cashflow.png")

plt.close()
# ----------------------------------------
# PDF
# ----------------------------------------

pdf = SimpleDocTemplate(
    "output/TCS_Tearsheet.pdf",
    pagesize=(8.27 * inch, 11.69 * inch)
)

story = []

# ===================================================
# PAGE 1
# ===================================================

header = Table(
    [[f"{company.iloc[0]['company_name']} ({COMPANY})"]],
    colWidths=[7.5 * inch]
)

header.setStyle(
    TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.navy),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.white),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 20),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("ALIGN", (0,0), (-1,-1), "CENTER")
    ])
)

story.append(header)
story.append(Spacer(1,20))

# ===================================================
# KPI Tiles
# ===================================================

story.append(
    Paragraph(
        "<b>Key Financial Metrics</b>",
        title_style
    )
)

story.append(Spacer(1,10))

kpi_data = [

    [

        f"<b>Sales</b><br/>{latest_fin['sales']}",

        f"<b>Net Profit</b><br/>{latest_fin['net_profit']}",

        f"<b>EPS</b><br/>{latest_fin['eps']}"

    ],

    [

        f"<b>ROE</b><br/>{round(latest_ratio['return_on_equity_pct'],2)}%",

        f"<b>Debt / Equity</b><br/>{round(latest_ratio['debt_to_equity'],2)}",

        f"<b>Net Margin</b><br/>{round(latest_ratio['net_profit_margin_pct'],2)}%"

    ]

]

kpi_table = Table(
    kpi_data,
    colWidths=[2.4*inch]*3,
    rowHeights=[0.9*inch]*2
)

kpi_table.setStyle(

    TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),colors.whitesmoke),

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BOX",(0,0),(-1,-1),1,colors.black),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,-1),10),

        ("TOPPADDING",(0,0),(-1,-1),10)

    ])

)

story.append(kpi_table)

story.append(Spacer(1,20))

# ===================================================
# Placeholder for Charts
# ===================================================

story.append(
    Paragraph(
        "<b>Charts will be added in Part 3</b>",
        normal
    )
)

story.append(Spacer(1,20))

story.append(Paragraph("<b>Financial Charts</b>", title_style))

story.append(Spacer(1,10))
table = Table(

    [

        [

            Image(
                "output/charts/revenue.png",
                width=3.3*inch,
                height=2.2*inch
            ),

            Image(
                "output/charts/netprofit.png",
                width=3.3*inch,
                height=2.2*inch
            )

        ],

        [

            Image(
                "output/charts/roe.png",
                width=3.3*inch,
                height=2.2*inch
            ),

            Image(
                "output/charts/roce.png",
                width=3.3*inch,
                height=2.2*inch
            )

        ]

    ],

    colWidths=[3.5*inch,3.5*inch]

)

story.append(table)

story.append(PageBreak())

# ===================================================
# PAGE 2
# ===================================================

header2 = Table(
    [["Additional Analysis"]],
    colWidths=[7.5*inch]
)

header2.setStyle(
    TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),colors.navy),
        ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),18),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),10),
        ("ALIGN",(0,0),(-1,-1),"CENTER")
    ])
)

story.append(header2)
story.append(Spacer(1,15))

# ------------------------------------
# Balance Sheet Chart
# ------------------------------------

story.append(
    Paragraph(
        "<b>Balance Sheet Composition</b>",
        title_style
    )
)

story.append(
    Image(
        "output/charts/balance_sheet.png",
        width=6.5*inch,
        height=3*inch
    )
)

story.append(Spacer(1,15))

# ------------------------------------
# Cash Flow Chart
# ------------------------------------

story.append(
    Paragraph(
        "<b>Latest Cash Flow</b>",
        title_style
    )
)

story.append(
    Image(
        "output/charts/cashflow.png",
        width=6.5*inch,
        height=3*inch
    )
)

story.append(Spacer(1,15))

# ------------------------------------
# Pros
# ------------------------------------

story.append(
    Paragraph(
        "<font color='green'><b>Pros</b></font>",
        title_style
    )
)

pros = pros_cons[
    (pros_cons["company_id"] == COMPANY) &
    (pros_cons["type"] == "pro")
]

for row in pros.head(5).itertuples():
    story.append(
        Paragraph(
            "• " + row.text,
            normal
        )
    )

story.append(Spacer(1,12))

# ------------------------------------
# Cons
# ------------------------------------

story.append(
    Paragraph(
        "<font color='red'><b>Cons</b></font>",
        title_style
    )
)

cons = pros_cons[
    (pros_cons["company_id"] == COMPANY) &
    (pros_cons["type"] == "con")
]

for row in cons.head(5).itertuples():
    story.append(
        Paragraph(
            "• " + row.text,
            normal
        )
    )

story.append(Spacer(1,15))

# ------------------------------------
# Capital Allocation Badge
# ------------------------------------

latest_pattern = (
    capital[
        capital["company_id"] == COMPANY
    ]
    .sort_values("year")
    .iloc[-1]["pattern_label"]
)

badge = Table(
    [[f"Capital Allocation : {latest_pattern}"]],
    colWidths=[5*inch]
)

badge.setStyle(
    TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),14),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),8),
    ])
)

story.append(badge)
pdf.build(story)

print("=" * 50)
print("PDF Generated Successfully")
print("=" * 50)
print("Saved to output/TCS_Tearsheet.pdf")