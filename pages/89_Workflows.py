
# pages/89_Workflows.py
import streamlit as st
import store
from ui_chrome import apply_chrome
apply_chrome()  # idempotent

store.init()
st.title("Workflows")

lead_id = store.get_selected_lead_id()
if not lead_id:
    st.info("Select a client in Client Record first.")
    st.stop()

lead = store.get_lead(lead_id)
st.caption(f"Client: {lead.get('name','—')} ({lead.get('id','—')}) • {lead.get('city','—')} • Assigned: {lead.get('assigned_to') or '—'}")

intake_done = bool(lead.get("intake_completed"))

st.subheader("Intake")
st.write("Collect personal, care, financial, lifestyle.")
if st.button("Open Intake →", key="open_intake_hub"):
    st.session_state["_goto_page"] = "pages/90_Intake_Workflow.py"
    st.rerun()

st.subheader("Placement")
st.write("Shortlist communities, schedule tours, record outcomes.")
st.button(
    "Open Placement →",
    key="open_place_hub",
    disabled=not intake_done,
    on_click=lambda: (
        store.set_selected_lead(lead["id"]),
        st.session_state.update(_goto_page="pages/91_Placement_Workflow.py"),
        st.rerun()
    ),
)
if not intake_done:
    st.caption("Complete Intake first.")

st.subheader("Follow-up")
st.write("Post-placement check-ins and escalations.")
if st.button("Open Follow-up →", key="open_follow_hub"):
    st.session_state["_goto_page"] = "pages/92_Followup_Workflow.py"
    st.rerun()