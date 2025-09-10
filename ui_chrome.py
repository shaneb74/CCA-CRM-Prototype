# ui_chrome.py
import streamlit as st

def _consume_pending_redirect():
    """If a prior click scheduled a redirect, do it immediately on top-of-run."""
    dest = st.session_state.pop("_goto_page", None)
    if not dest:
        return
    try:
        if hasattr(st, "switch_page"):
            st.switch_page(dest)
    except Exception:
        # If switch_page isn't available, do nothing; user stays on current page.
        # We don't re-set the flag to avoid loops.
        pass

def set_wide():
    """Safe wide layout; ignore if already set elsewhere."""
    try:
        st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide")
    except Exception:
        pass

def decorate_sidebar_with_workflow_divider():
    """
    Visually separate workflow pages; assumes you've renamed them 90/91/92_*.
    """
    css = """
    <style>
      section[data-testid="stSidebar"] { --divider:#e5e7eb; --muted:#6b7280; }
      section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"]{
        margin-top:14px; padding-top:12px; border-top:1px solid var(--divider);
      }
      section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"]::before{
        content:"Workflows"; display:block; font-size:12px; color:var(--muted); margin-bottom:6px; letter-spacing:.02em;
      }
      section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"],
      section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="91_Placement_Workflow"],
      section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="92_Followup_Workflow"]{
        opacity:.95;
      }
      footer, #MainMenu { visibility:hidden; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def hide_default():
    """
    Backwards-compatible entry point many pages already import.
    Runs redirect consumption early, then minimal chrome.
    """
    _consume_pending_redirect()
    # Minimal chrome (kept here so old imports still have some effect)
    st.markdown("<style>footer,#MainMenu{visibility:hidden;}</style>", unsafe_allow_html=True)

def apply_chrome():
    """
    One call to rule them all. Use this if you want the full treatment.
    """
    _consume_pending_redirect()
    set_wide()
    decorate_sidebar_with_workflow_divider()