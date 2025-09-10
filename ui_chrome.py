# ui_chrome.py
import streamlit as st

def _set_wide(page_title: str | None, page_icon: str | None):
    try:
        st.set_page_config(
            page_title=page_title or "CCA CRM Prototype",
            page_icon=page_icon or "📋",
            layout="wide",
        )
    except Exception:
        # It's already been set on this run; ignore silently.
        pass

def _decorate_sidebar_group():
    css = """
    <style>
    section[data-testid="stSidebar"] { --divider:#e5e7eb; --muted:#6b7280; }
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"]{
        margin-top:14px; padding-top:12px; border-top:1px solid var(--divider);
    }
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"]::before{
        content:"Workflows"; display:block; font-size:12px; color:var(--muted);
        margin-bottom:6px; letter-spacing:.02em;
    }
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"],
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="91_Placement_Workflow"],
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][href*="92_Followup_Workflow"]{
        opacity:.95;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def _consume_pending_redirect():
    dest = st.session_state.pop("_goto_page", None)
    if dest:
        try:
            if hasattr(st, "switch_page"):
                st.switch_page(dest)
        except Exception:
            pass

def apply_chrome(page_title: str | None = None, page_icon: str | None = None):
    """Call this as the first lines of every page."""
    _set_wide(page_title, page_icon)
    _consume_pending_redirect()
    _decorate_sidebar_group()