import streamlit as st
import store


st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide", initial_sidebar_state="expanded")
store.init()
st.title("CCA CRM Prototype")
st.caption("Dashboard → Advisor Workspace → Case Overview · Notifications")
