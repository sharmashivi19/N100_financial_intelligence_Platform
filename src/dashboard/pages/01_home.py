
import sys
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios
)
st.sidebar.title("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    [
        "Mar 2019",
        "Mar 2020",
        "Mar 2021",
        "Mar 2022",
        "Mar 2023",
        "Mar 2024"
    ]
)
companies = get_companies()
ratios = get_ratios()

ratios = ratios[
    ratios["year"] == year
]
st.title("Nifty 100 Analytics")

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Average ROE",
    round(ratios["return_on_equity_pct"].mean(),2)
)

c2.metric(
    "Median D/E",
    round(ratios["debt_to_equity"].median(),2)
)

c3.metric(
    "Companies",
    ratios["company_id"].nunique()
)

c4.metric(
    "Median Revenue CAGR",
    round(ratios["revenue_cagr_5yr"].median(),2)
)

c5.metric(
    "Debt Free",
    (ratios["debt_to_equity"]==0).sum()
)

c6.metric(
    "Avg Composite",
    round(
        ratios["composite_quality_score"].mean(),
        2
    )
)
peer = pd.read_excel(
    "data/source_files/peer_groups.xlsx"
)

df = ratios.merge(
    peer,
    on="company_id",
    how="left"
)

sector = (
    df.groupby("peer_group_name")
      .size()
      .reset_index(name="Count")
)

fig = px.pie(
    sector,
    names="peer_group_name",
    values="Count",
    hole=0.5,
    title="Peer Group Breakdown"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
top5 = ratios.sort_values(

    "composite_quality_score",

    ascending=False

).head(5)

st.subheader(
    "Top 5 Companies"
)

st.dataframe(top5)