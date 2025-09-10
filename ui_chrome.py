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
    # Fallback: do nothing (Cloud rerun will keep state; links still work from hub).

def _decorate_sidebar_workflows():
    # Visually group 90/91/92 workflow pages under a divider + label
    css = """
    <style>
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="pages/90_"]{
      margin-top:14px; padding-top:12px; border-top:1px solid #e5e7eb;
    }
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="pages/90_"]::before{
      content:"Workflows"; display:block; font-size:12px; color:#6b7280; margin-bottom:6px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def hide_workflow_pages():
    """Hide workflow pages from the sidebar."""
    st.hide_pages([
        "88_Workflows_Section",
        "89_Workflows",
        "90_Intake_Workflow",
        "91_Placement_Workflow",
        "92_Followup_Workflow",
    ])

def apply_chrome():
    _safe_set_page_config()
    hide_workflow_pages()  # Hide pages after page config, before rendering
    _consume_redirect()
    _decorate_sidebar_workflows()
