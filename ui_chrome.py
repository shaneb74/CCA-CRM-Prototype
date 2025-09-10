# ui_chrome.py — CSS helper to hide specific pages from the sidebar
import streamlit as st
def hide_pages(hrefs: list[str]):
    if not hrefs: return
    sels = ",".join([f'section[data-testid="stSidebar"] a[href*="{h}"]' for h in hrefs])
    st.markdown(f"<style>{sels}{{display:none!important;}}</style>", unsafe_allow_html=True)