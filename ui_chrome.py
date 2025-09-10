# ui_chrome.py
import streamlit as st

def set_wide():
    # Safe even if called multiple times or not first
    try:
        st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide")
    except Exception:
        pass

def hide_default():
    """Keep whatever you already hide (toolbar, footer, etc.)."""
    css = """
    <style>
      footer {visibility:hidden;}
      #MainMenu {visibility:hidden;}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def hide_workflow_nav():
    """
    Hide workflow pages from the left nav everywhere:
    - 00_Workflows.py
    - 06_Intake_Workflow.py
    - 07_Placement_Workflow.py
    - 08_Followup_Workflow.py
    This relies on the file name appearing in the link href (Streamlit default).
    """
    selectors = [
        "00_Workflows",
        "06_Intake_Workflow",
        "07_Placement_Workflow",
        "08_Followup_Workflow",
    ]
    css_rules = "\n".join(
        [f"""a[data-testid="stSidebarNavLink"][href*="{name}"] {{ display: none !important; }}"""
         for name in selectors]
    )
    st.markdown(f"<style>{css_rules}</style>", unsafe_allow_html=True)

def apply_chrome():
    """One call to rule them all: wide + default hides + workflow hides."""
    set_wide()
    hide_default()
    hide_workflow_nav()
