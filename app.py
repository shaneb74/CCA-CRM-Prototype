import streamlit as st
import store
st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide", initial_sidebar_state="expanded")
store.init()
st.title("CCA CRM Prototype")
st.caption("Dashboard → Advisor Workspace → Case Overview · Notifications")

# Hide the Streamlit menu, footer, and header
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
