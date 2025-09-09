import streamlit as st
from ui.widgets import inject_css

st.set_page_config(page_title="Senior CRM Prototype", page_icon="📋", layout="wide")
inject_css()

st.markdown("# app")
st.markdown("Use the left nav to open pages.")
