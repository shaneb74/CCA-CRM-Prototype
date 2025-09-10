
# ui_chrome.py — tiny helpers for UI chrome tweaks
import streamlit as st

def hide_sidebar_page(href_substring: str):
    """Hide a sidebar nav link whose href contains the given substring.
    Example: hide_sidebar_page("00_Workflows")
    """
    css = f"""
    <style>
    section[data-testid="stSidebar"] a[href*="{href_substring}"] {{
        display: none !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
