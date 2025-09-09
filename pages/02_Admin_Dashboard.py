
import streamlit as st
from ui.widgets import kpi
st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
kpi("App status", "OK")
