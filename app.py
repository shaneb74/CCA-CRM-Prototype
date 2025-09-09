
import streamlit as st
from ui.widgets import inject_css

st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide")
inject_css()
st.title("CCA CRM Prototype")
st.caption("Advisor Workspace rework — compact, dense, and skimmable.")

st.page_link("pages/01_Advisor_Workspace.py", label="Open Advisor Workspace")
st.page_link("pages/03_🔔_Notifications.py", label="Open Notifications")
