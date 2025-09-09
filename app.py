
import streamlit as st
from ui.widgets import section

st.set_page_config(page_title="Senior CRM Prototype", page_icon="📋", layout="wide")
st.title("Senior CRM Prototype")
st.caption("Now with a notifications drawer and collapsible sections (mock).")

col1, col2 = st.columns(2)
with col1:
    section("Dashboards")
    st.page_link("pages/01_Advisor_Dashboard_Mock.py", label="Advisor dashboard (mock w/ drawer)")
with col2:
    section("Demos")
    st.page_link("pages/11_Client_Record.py", label="Client Record (demo)")
