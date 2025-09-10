import streamlit as st

def set_wide():
    try:
        st.set_page_config(page_title="CCA CRM Prototype", page_icon="📋", layout="wide")
    except Exception:
        pass

def decorate_sidebar_with_workflow_divider():
    """
    Adds a horizontal rule and a 'Workflows' label above the first workflow link,
    and keeps all workflow links visually grouped.
    This targets files renamed to 90/91/92_* as suggested.
    """
    css = """
    <style>
    /* Sidebar base selector */
    section[data-testid="stSidebar"] {
      --divider: #e5e7eb;      /* light gray */
      --muted: #6b7280;        /* gray-500 */
    }

    /* Add a group label + divider above the first workflow link */
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"] {
        margin-top: 14px;
        padding-top: 12px;
        border-top: 1px solid var(--divider);
    }
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"]::before {
        content: "Workflows";
        display: block;
        font-size: 12px;
        color: var(--muted);
        margin-bottom: 6px;
        letter-spacing: .02em;
        text-transform: none;
    }

    /* Slightly mute the workflow items so the group reads as secondary */
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="90_Intake_Workflow"],
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="91_Placement_Workflow"],
    section[data-testid="stSidebar"]
      a[data-testid="stSidebarNavLink"][href*="92_Followup_Workflow"] {
        opacity: 0.95;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def apply_chrome():
    set_wide()
    decorate_sidebar_with_workflow_divider()


def consume_pending_redirect():
    """If a prior click scheduled a redirect, do it now on top-of-run."""
    dest = st.session_state.pop("_goto_page", None)
    if dest:
        try:
            if hasattr(st, "switch_page"):
                st.switch_page(dest)
        except Exception:
            pass  # worst case, we just ignore

def apply_chrome():
    # whatever you already do...
    try:
        consume_pending_redirect()
    except Exception:
        pass