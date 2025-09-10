# ui_chrome.py — central place to hide workflow pages from sidebar
import streamlit as st
HIDDEN = ["00_Workflows", "06_Intake_Workflow", "07_Placement_Workflow", "08_Followup_Workflow"]
def hide_default():
    if not HIDDEN: 
        return
    selectors = ",".join([f'section[data-testid="stSidebar"] a[href*="{h}"]' for h in HIDDEN])
    st.markdown(f"<style>{selectors}{{display:none!important;}}</style>", unsafe_allow_html=True)