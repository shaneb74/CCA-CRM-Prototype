import streamlit as st

# --- one-time guard for page_config across the whole app ---
def _guard_page_config():
    """
    Monkey-patch st.set_page_config so only the FIRST call in a run does real work.
    Subsequent calls become harmless no-ops. This prevents StreamlitAPIException
    when pages accidentally call st.set_page_config more than once.
    """
    if getattr(st, "_cca_pgcfg_guarded", False):
        return

    # Keep the original (in case we ever need it)
    if not hasattr(st, "_cca_orig_set_page_config"):
        st._cca_orig_set_page_config = st.set_page_config

    def _first_only(*args, **kwargs):
        # If already applied once, ignore further calls
        if getattr(st, "_cca_pgcfg_applied", False):
            return None
        # Call the real thing once
        st._cca_orig_set_page_config(*args, **kwargs)
        st._cca_pgcfg_applied = True
        return None

    st.set_page_config = _first_only
    st._cca_pgcfg_guarded = True


def _apply_base_config():
    """
    Set app-wide defaults for title/icon/layout ONCE (safe to call on every page).
    """
    try:
        st.set_page_config(
            page_title="CCA CRM Prototype",
            page_icon="📋",
            layout="wide",
        )
    except Exception:
        # With our guard in place, exceptions are unlikely, but be defensive.
        pass


def _consume_redirect():
    """
    If a previous button scheduled a redirect (via st.session_state['_goto_page']),
    perform it exactly once at the top of a run.
    """
    dest = st.session_state.pop("_goto_page", None)
    if not dest:
        return
    try:
        if hasattr(st, "switch_page"):
            st.switch_page(dest)
    except Exception:
        # If switch_page isn't available, we fail silently; links from hubs still work.
        pass


def apply_chrome():
    """
    Call this at the TOP of every page, before rendering any UI.
    It:
      1) Installs the page_config guard (prevents duplicate calls from blowing up)
      2) Applies the base page config (title/icon/layout) once per run
      3) Consumes any pending redirect
    """
    _guard_page_config()
    _apply_base_config()
    _consume_redirect()
