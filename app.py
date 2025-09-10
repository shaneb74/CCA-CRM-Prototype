import streamlit as st
import store

def boot():
    st.hide_pages([
        "88_Workflows_Section",
        "89_Workflows",
        "90_Intake_Workflow",
        "91_Placement_Workflow",
        "92_Followup_Workflow",
    ])

st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide", initial_sidebar_state="expanded")
boot()  # Hide pages before sidebar renders
store.init()

st.title("CCA CRM Prototype")
st.caption("Dashboard → Advisor Workspace → Case Overview · Notifications")
