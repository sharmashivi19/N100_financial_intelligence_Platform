import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_financials
)
companies = get_companies()

selected = st.selectbox(

    "Search Company",

    companies["company_name"]

)
company = companies[
    companies["company_name"]==selected
].iloc[0]

st.title(company["company_name"])

st.write(company["about_company"])
ratios = get_ratios()

company_ratios = ratios[
    ratios["company_id"]==company["id"]
]
latest = company_ratios.iloc[-1]

c1,c2,c3 = st.columns(3)

c1.metric(

    "ROE",

    round(
        latest["return_on_equity_pct"],
        2
    )
)

c2.metric(

    "Net Margin",

    round(
        latest["net_profit_margin_pct"],
        2
    )
)

c3.metric(

    "Debt/Equity",

    round(
        latest["debt_to_equity"],
        2
    )
)
financials = get_financials()

company_fin = financials[
    financials["company_id"]==company["id"]
]

fig = px.bar(

    company_fin,

    x="year",

    y=["sales","net_profit"]

)

st.plotly_chart(fig)
fig = px.line(

    company_ratios,

    x="year",

    y=[
        "return_on_equity_pct"
    ]

)

st.plotly_chart(
    fig,
    width="stretch"
)
if company_ratios.empty:

    st.warning(

        "Ticker not found — please try another."

    )

    st.stop()