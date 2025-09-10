
# 00_Workflows.py — Workflows hub (hidden from sidebar)
import streamlit as st
import store
from ui_chrome import hide_sidebar_page

# Hide this page from the left nav (but keep it routable)
hide_sidebar_page("00_Workflows")

store.init()
st.set_page_config(page_title="Workflows", page_icon="🧭", layout="wide")

st.title("Workflows")

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

if not lead:
    st.info("Select a client in Client Record first.")
    st.stop()

st.markdown(f"**Client:** {lead['name']} ({lead['id']}) • {lead['city']}  |  Assigned: {lead.get('assigned_to') or 'Unassigned'}")

mine = ((lead.get("assigned_to") or "").strip().lower()
        == (store.CURRENT_USER or "").strip().lower())

c1, c2, c3 = st.columns(3)
with c1:
    st.header("Intake")
    st.write("Gather initial info: personal, housing, medical, financial, lifestyle.")
    st.button("Set context for Intake", key="wf_intake_ctx",
              on_click=lambda: st.session_state.update(intake_lead_id=lead['id']),
              disabled=not mine, help=None if mine else "Only assigned advisor can run intake.")
    if hasattr(st, "page_link"):
        st.page_link("pages/06_Intake_Workflow.py", label="Open Intake →")
with c2:
    st.header("Placement")
    st.write("Shortlist communities, schedule tours, record outcomes.")
    if hasattr(st, "page_link"):
        st.page_link("pages/07_Placement_Workflow.py", label="Open Placement →")
with c3:
    st.header("Follow-up")
    st.write("Post-placement check-ins and escalations.")
    if hasattr(st, "page_link"):
        st.page_link("pages/08_Followup_Workflow.py", label="Open Follow-up →")
