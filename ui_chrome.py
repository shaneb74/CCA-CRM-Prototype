
import streamlit as st

_GUARD_KEY = "_page_config_applied"

def _safe_set_page_config(page_title: str, page_icon: str, layout: str):
    if st.session_state.get(_GUARD_KEY):
        return
    try:
        st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    except Exception:
        pass
    st.session_state[_GUARD_KEY] = True

def _consume_redirect():
    dest = st.session_state.pop("_goto_page", None)
    if not dest:
        return
    try:
        if hasattr(st, "switch_page"):
            st.switch_page(dest)
    except Exception:
        pass

def _decorate_sidebar():
    st.markdown("<style>\nsection[data-testid='stSidebar'] a[data-testid='stSidebarNavLink'][href*='90_']{margin-top:14px; padding-top:12px; border-top:1px solid #e5e7eb;}\nsection[data-testid='stSidebar'] a[data-testid='stSidebarNavLink'][href*='90_']::before{content:'Workflows'; display:block; font-size:12px; color:#6b7280; margin-bottom:6px;}\n</style>", unsafe_allow_html=True)

def apply_chrome(page_title: str = "CCA CRM Prototype", page_icon: str = "📋", layout: str = "wide"):
    _safe_set_page_config(page_title, page_icon, layout)
    _consume_redirect()
    _decorate_sidebar()
