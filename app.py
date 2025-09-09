
import streamlit as st
from ui.widgets import section
st.set_page_config(page_title="Senior CRM Prototype", page_icon="📋", layout="wide")
st.title("Senior CRM Prototype")
st.caption("Includes a **mock visual dashboard** to tune hierarchy without touching logic.")

col1, col2 = st.columns(2)
with col1:
    section("Dashboards")
    st.page_link("pages/01_Advisor_Dashboard.py", label="Advisor dashboard (current)")
    st.page_link("pages/01_Advisor_Dashboard_Mock.py", label="Advisor dashboard (visual mock)")
with col2:
    section("Other modules")
    st.page_link("pages/11_Client_Record.py", label="Client: Margaret Holt (demo)")
    st.page_link("pages/20_Communities.py", label="Communities")
