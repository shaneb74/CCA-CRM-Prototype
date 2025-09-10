
# ui_chrome.py — helpers for hiding sidebar pages
import streamlit as st

def hide_pages(hrefs: list[str]):
    """Hide any sidebar link whose href contains one of the given substrings.
    Example: hide_pages(["00_Workflows", "06_Intake_Workflow"])"""
    if not hrefs:
        return
    selectors = ",".join([f'section[data-testid="stSidebar"] a[href*="{h}"]' for h in hrefs])
    css = f"""<style>{selectors} {{ display: none !important; }}</style>"""
    st.markdown(css, unsafe_allow_html=True)
