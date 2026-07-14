import streamlit as st
import os

st.title("📄 Reports")

files = [
    "output/screener_output.xlsx",
    "output/peer_comparison.xlsx"
]

for file in files:

    if os.path.exists(file):

        with open(file, "rb") as f:

            st.download_button(

                label=f"Download {os.path.basename(file)}",

                data=f,

                file_name=os.path.basename(file)

            )

    else:

        st.warning(f"{file} not found.")