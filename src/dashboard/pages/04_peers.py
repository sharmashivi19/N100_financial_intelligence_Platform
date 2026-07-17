import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

st.title("👥 Peer Comparison")

# -----------------------------
# Load Data
# -----------------------------
conn = sqlite3.connect("database/nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

peer = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

conn.close()

# -----------------------------
# Load Peer Groups Excel
# -----------------------------
peer_groups = pd.read_excel(
    "data/source_files/peer_groups.xlsx"
)

# -----------------------------
# Merge Data
# -----------------------------
df = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

df = df.merge(
    peer_groups,
    on="company_id",
    how="left"
)

# -----------------------------
# Peer Group Dropdown
# -----------------------------
groups = sorted(
    df["peer_group_name"]
      .dropna()
      .unique()
)

selected_group = st.selectbox(
    "Select Peer Group",
    groups
)

group_df = df[
    df["peer_group_name"] == selected_group
]

# -----------------------------
# Company Dropdown
# -----------------------------
company = st.selectbox(
    "Select Company",
    sorted(group_df["company_name"].unique())
)

company_df = group_df[
    group_df["company_name"] == company
]

latest = company_df.sort_values(
    "year"
).iloc[-1]

# -----------------------------
# Metrics
# -----------------------------
metrics = [
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score"
]

labels = [
    "ROE",
    "OPM",
    "NPM",
    "D/E",
    "FCF",
    "PAT CAGR",
    "Revenue CAGR",
    "Composite"
]

company_values = [
    latest[m] if pd.notna(latest[m]) else 0
    for m in metrics
]

peer_values = [
    group_df[m].mean()
    for m in metrics
]

# close polygon
company_values.append(company_values[0])
peer_values.append(peer_values[0])
labels.append(labels[0])

# -----------------------------
# Radar Chart
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=labels,
        fill="toself",
        name=company
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=labels,
        mode="lines",
        line=dict(dash="dash"),
        name="Peer Average"
    )
)

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=650
)

st.plotly_chart(
    fig,
    width="stretch"
)

# -----------------------------
# KPI Table
# -----------------------------
st.subheader("Peer Group Companies")

table = (
    group_df[
        [
            "company_name",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "composite_quality_score",
            "is_benchmark"
        ]
    ]
    .drop_duplicates("company_name")
)

def highlight(row):
    if row["is_benchmark"]:
        return [
            "background-color: gold"
        ] * len(row)
    return [
        ""
    ] * len(row)

st.dataframe(
    table.style.apply(
        highlight,
        axis=1
    ),
    use_container_width=True
)