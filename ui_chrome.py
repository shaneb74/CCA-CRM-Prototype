# ui_chrome.py
import streamlit as st

# --- single-run guards ---
def _once_key()->str:
    return "_page_config_applied"

def _safe_set_page_config():
    if st.session_state.get(_once_key()):
        return
    try:
        st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide")
    except Exception:
        # Already set elsewhere in the same run — ignore
        pass
    st.session_state[_once_key()] = True

def _consume_redirect():
    """If a previous click asked us to go somewhere, do it once at start of run."""
    dest = st.session_state.pop("_goto_page", None)
    if not dest:
        return
    try:
        if hasattr(st, "switch_page"):
            st.switch_page(dest)
            return
    except Exception:
        pass
    # Fallback: do nothing; next run will still work via buttons.

def _decorate_sidebar_workflows():
    # Optional: visually group workflow pages under a divider + label
    css = """
    <style>
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="90_"]{
      margin-top:14px; padding-top:12px; border-top:1px solid #e5e7eb;
    }
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="90_"]::before{
      content:"Workflows"; display:block; font-size:12px; color:#6b7280; margin-bottom:6px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def _hide_workflow_links():
    """
    Actually hide workflow links from the sidebar by removing the anchors.
    Important: do NOT include `pages/` in the href match. Streamlit uses paths like `/90_Intake_Workflow`.
    """
    css = """
    <style>
    /* Remove the anchors entirely (collapses the row) */
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"],
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="91_Placement_Workflow"],
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="92_Followup_Workflow"],
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="88_Workflows_Section"],
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="89_Workflows"] {
        display: none !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def apply_chrome(hide_workflows: bool = True, show_workflow_divider: bool = False):
    _safe_set_page_config()
    _consume_redirect()
    # Order matters: if you hide items, you probably don't want the divider label
    if hide_workflows:
        _hide_workflow_links()
    if show_workflow_divider and not hide_workflows:
        _decorate_sidebar_workflows()
