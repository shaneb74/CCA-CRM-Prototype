
import streamlit as st
from ui.widgets import section
st.set_page_config(page_title="Senior CRM Prototype", page_icon="📋", layout="wide")
st.title("Senior CRM Prototype")
st.caption("Click-through prototype focused on dashboard presentation and navigation.")
col1, col2 = st.columns(2)
with col1:
    section("Start as…")
    st.page_link("pages/01_Advisor_Dashboard.py", label="Advisor dashboard")
    st.page_link("pages/11_Client_Record.py", label="Client: Margaret Holt (demo)")
    st.page_link("pages/20_Communities.py", label="Communities")
    st.page_link("pages/30_Prospects.py", label="Prospects")
with col2:
    section("Admin & Tools…")
    st.page_link("pages/02_Admin_Dashboard.py", label="Admin dashboard")
    st.page_link("pages/40_Decision_Support.py", label="Decision Support (mock)")
    st.page_link("pages/50_Documents.py", label="Documents")
    st.page_link("pages/60_Reports.py", label="Reports")
