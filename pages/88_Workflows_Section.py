import streamlit as st
from ui_chrome import apply_chrome
apply_chrome()

st.set_page_config(page_title="— Workflows —", page_icon="•", layout="wide")
# Uncomment to bounce back to Dashboard:
# if hasattr(st, "switch_page"):
#     st.switch_page("pages/01_Dashboard.py")