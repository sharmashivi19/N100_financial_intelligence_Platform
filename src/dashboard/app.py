import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty 100 Analytics")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Company Profile",
        "Screener",
        "Peer Comparison",
        "Financial Trends",
        "Sector Analysis",
        "Capital Allocation",
        "Reports"
    ]
)

st.header(page)

st.write(f"Welcome to the {page} page.")