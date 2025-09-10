
# ui_chrome.py — CSS-only sidebar hider (v3, no <script> required)
import streamlit as st

def hide_default():
    """
    Hide workflow pages from the sidebar purely with CSS attribute selectors.
    Works even when Streamlit sanitizes <script> tags.
    """
    # common URL fragments Streamlit generates (covering both file-path and slugged urls)
    fragments = [
        "00_Workflows", "workflows",
        "06_Intake_Workflow", "intake-workflow", "intake_workflow",
        "07_Placement_Workflow", "placement-workflow", "placement_workflow",
        "08_Followup_Workflow", "followup-workflow", "followup_workflow",
    ]

    selectors = []
    for frag in fragments:
        # Typical sidebar structure: section[data-testid="stSidebar"] a[href*="..."]
        selectors.append(f'section[data-testid="stSidebar"] a[href*="{frag}"]')
        # Also hide the parent li (anchor is usually inside a list item)
        selectors.append(f'section[data-testid="stSidebar"] a[href*="{frag}"] *')

    css = ",".join(selectors) + "{display:none !important;visibility:hidden !important;}"

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
