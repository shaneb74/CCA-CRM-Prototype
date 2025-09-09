
import streamlit as st
from ui.widgets import section, kpi, table
from data_loader import load_seed

st.set_page_config(page_title="Senior CRM Prototype", page_icon="📋", layout="wide")

st.title("Senior CRM Prototype (Ultra-lean)")
st.caption("No external deps. If this doesn't boot, it's not the code.")

col1, col2 = st.columns(2)
with col1:
    section("Start as…")
    st.page_link("pages/01_Advisor_Dashboard.py", label="Advisor dashboard")
    st.page_link("pages/10_Clients.py", label="Clients")
with col2:
    section("Admin & Setup…")
    st.page_link("pages/02_Admin_Dashboard.py", label="Admin dashboard")
    st.page_link("pages/60_Reports.py", label="Reports")
