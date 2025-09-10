
# ui_chrome.py — helpers for hiding sidebar pages via CSS
import streamlit as st

def hide_pages(hrefs: list[str]):
    """Hide any sidebar link whose href contains any of the given substrings."""
    if not hrefs:
        return
    selectors = ",".join([f'section[data-testid="stSidebar"] a[href*="{h}"]' for h in hrefs])
    st.markdown(f"""<style>{selectors} {{ display: none !important; }}</style>""", unsafe_allow_html=True)
