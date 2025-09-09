
import streamlit as st
from ui.widgets import inject_css
inject_css()

st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide")
st.title("CCA CRM Prototype")

st.page_link("pages/01_Advisor_Workspace.py", label="Advisor Workspace")
st.page_link("pages/02_Advisor_Dashboard_Mock.py", label="Advisor Dashboard Mock")
st.page_link("pages/03_🔔_Notifications.py", label="🔔 Notifications")
st.page_link("pages/10_Admin_Dashboard.py", label="Admin Dashboard")
st.page_link("pages/20_Clients.py", label="Clients")
st.page_link("pages/21_Client_Record.py", label="Client Record")
st.page_link("pages/30_Communities.py", label="Communities")
st.page_link("pages/40_Prospects.py", label="Prospects")
st.page_link("pages/50_Decision_Support.py", label="Decision Support")
st.page_link("pages/60_Documents.py", label="Documents")
st.page_link("pages/70_Reports.py", label="Reports")
