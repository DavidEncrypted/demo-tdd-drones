"""Streamlit webapp entry point."""

import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Drone Flight Analysis",
    page_icon="🚁",
)

page = st.navigation(
    {
        "Flight Data": [
            st.Page("src/webapp/robolog/summary.py", title="Summary"),
            st.Page("src/webapp/robolog/plot.py", title="Plot"),
        ],
    },
    position="sidebar",
)

page.run()
