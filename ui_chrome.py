
# ui_chrome.py  — safe page config + sidebar grouping + redirect hook
import streamlit as st

def page_config(title: str, icon: str = "📋", layout: str = "wide"):
    """Safe wrapper around st.set_page_config; only runs once per session."""
    flag = "_cca_cfg_set"
    if not st.session_state.get(flag):
        try:
            st.set_page_config(page_title=title, page_icon=icon, layout=layout)
        except Exception:
            pass
        st.session_state[flag] = True

def _consume_pending_redirect():
    dest = st.session_state.pop("_goto_page", None)
    if not dest:
        return
    try:
        if hasattr(st, "switch_page"):
            st.switch_page(dest)
        else:
            st.experimental_rerun()
    except Exception:
        pass

def _decorate_sidebar_with_workflow_divider():
    css = """
    <style>
      section[data-testid="stSidebar"]
        a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"]{
          margin-top:14px; padding-top:12px; border-top:1px solid #e5e7eb;
        }
      section[data-testid="stSidebar"]
        a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"]::before{
          content:"Workflows"; display:block; font-size:12px; color:#6b7280;
          margin-bottom:6px; letter-spacing:.02em;
        }
    </style>
    """
    try:
        import streamlit as st
        st.markdown(css, unsafe_allow_html=True)
    except Exception:
        pass

def apply_chrome(title: str = None, icon: str = "📋", layout: str = "wide"):
    """Call this first thing on every page."""
    _consume_pending_redirect()
    if title:
        page_config(title, icon, layout)
    _decorate_sidebar_with_workflow_divider()
