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

    st.set_page_config(page_title="Workflows", page_icon="🧭", layout="wide")
    store.init()

    lead_id = store.get_selected_lead_id()
    st.title("Workflows")

    if not lead_id:
        st.info("Select a client in **Client Record** first.")
        st.stop()

    lead = store.get_lead(lead_id) or {'id': lead_id, 'name': 'Unknown', 'city':'–', 'assigned_to':'–'}

    st.caption(f"**Client:** {lead['name']} ({lead['id']}) • {lead.get('city','–')} • **Assigned:** {lead.get('assigned_to','–')}")

    st.subheader("Intake")
    st.write("Collect personal, care, financial, lifestyle.")
    if st.button("Open Intake →", key="open_intake"):
        if hasattr(st, "switch_page"):
            st.switch_page("pages/90_Intake_Workflow.py")

    st.subheader("Placement")
    st.write("Shortlist communities, schedule tours, record outcomes.")
    if st.button("Open Placement →", key="open_placement"):
        if hasattr(st, "switch_page"):
            st.switch_page("pages/91_Placement_Workflow.py")

    st.subheader("Follow-up")
    st.write("Post-placement check-ins and escalations.")
    if st.button("Open Follow-up →", key="open_followup"):
        if hasattr(st, "switch_page"):
            st.switch_page("pages/92_Followup_Workflow.py")
