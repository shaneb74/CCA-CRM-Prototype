# --- path bootstrap so root modules import from /pages scripts ---
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# optional chrome tweaks (safe if missing)
try:
    from ui_chrome import hide_default
    hide_default()
except Exception:
    pass

    import streamlit as st
    import store

    st.set_page_config(page_title="Placement Workflow", page_icon="📍", layout="wide")
    store.init()
    lead_id = store.get_selected_lead_id()
    st.title("Placement Workflow")

    if not lead_id:
        st.info("No client selected. Use **Client Record** or the **Workflows** hub.")
        st.stop()

    lead = store.get_lead(lead_id)
    st.caption(f"{lead['name']} • {lead.get('city','–')} • **Assigned:** {lead.get('assigned_to','–')}")

    st.write("Use this space for community shortlist & tour outcomes (mock).")

    if st.button("← Back to Workflows"):
        if hasattr(st, "switch_page"):
            st.switch_page("pages/89_Workflows.py")
