from ui_chrome import apply_chrome
apply_chrome()

import streamlit as st, store
store.init()

st.title("Workflows")

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

if not lead:
    st.info("Select a client in Client Record first.")
    st.stop()

st.caption(f"Client: **{lead.get('name','')}** ({lead.get('id')}) • {lead.get('city','')} • Assigned: **{lead.get('assigned_to') or 'Unassigned'}**")

st.subheader("Intake")
st.write("Collect personal, care, financial, lifestyle.")
if st.button("Open Intake →", key="open_intake"):
    st.session_state["_goto_page"]="pages/90_Intake_Workflow.py"
    st.experimental_rerun()

st.subheader("Placement")
st.write("Shortlist communities, schedule tours, record outcomes.")
if st.button("Open Placement →", key="open_place"):
    st.session_state["_goto_page"]="pages/91_Placement_Workflow.py"
    st.experimental_rerun()

st.subheader("Follow-up")
st.write("Post-placement check-ins and escalations.")
if st.button("Open Follow-up →", key="open_follow"):
    st.session_state["_goto_page"]="pages/92_Followup_Workflow.py"
    st.experimental_rerun()
