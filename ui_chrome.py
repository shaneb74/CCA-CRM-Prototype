
# ui_chrome.py — small CSS helper to hide sidebar entries for given pages
import streamlit as st

def hide_pages(hrefs: list[str]):
    if not hrefs:
        return
    selectors = ",".join([f'section[data-testid="stSidebar"] a[href*="{h}"]' for h in hrefs])
    st.markdown(f"<style>{selectors} {{ display: none !important; }}</style>", unsafe_allow_html=True)
