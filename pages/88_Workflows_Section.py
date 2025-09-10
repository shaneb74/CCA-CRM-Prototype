import streamlit as st
st.set_page_config(page_title="— Workflows —", page_icon="•", layout="wide")
if hasattr(st, "switch_page"):
    st.switch_page("pages/01_Dashboard.py")