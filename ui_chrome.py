
import streamlit as st

def apply_chrome():
    """Safe, argument-free helper used at top of every page.
    - Sets wide layout
    - Draws a divider + label above numbered workflow pages (90/91/92)
    - Consumes any pending redirect scheduled via st.session_state["_goto_page"]
    """
    try:
        st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide")
    except Exception:
        pass

    # visual group for workflow pages (works with renamed 90/91/92 files)
    css = """
    <style>
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"] {
        margin-top: 14px; padding-top: 12px; border-top: 1px solid #e5e7eb;
    }
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"]::before {
        content: "Workflows"; display:block; font-size:12px; color:#6b7280; margin-bottom:6px;
    }
    </style>
    """
    try:
        st.markdown(css, unsafe_allow_html=True)
    except Exception:
        pass

    # handle scheduled redirects (used by buttons that set _goto_page)
    dest = st.session_state.pop("_goto_page", None)
    if dest:
        try:
            if hasattr(st, "switch_page"):
                st.switch_page(dest)
        except Exception:
            # fallback: no-op
            pass
