
# pages/89_Workflows.py
# Hub page with reliable links
import streamlit as st
import store

st.set_page_config(page_title="Workflows", page_icon="🧩", layout="wide")
store.init()

lead_id = store.get_selected_lead_id()
st.title("Workflows")

if not lead_id:
    st.info("Select a client in Client Record first.")
    st.stop()

lead = store.get_lead(lead_id)
if not lead:
    st.info("Select a client in Client Record first.")
    st.stop()

st.caption(f"Client: {lead.get('name')} ({lead.get('id')}) • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

c1,c2,c3 = st.columns(3)
with c1:
    st.subheader("Intake")
    st.write("Collect personal, care, financial, lifestyle.")
    if st.button("Open Intake →", key="open_intake"):
        st.session_state["_goto_page"] = "pages/90_Intake_Workflow.py"
        st.experimental_rerun()
with c2:
    st.subheader("Placement")
    st.write("Shortlist communities, schedule tours, record outcomes.")
    if st.button("Open Placement →", key="open_placement"):
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.experimental_rerun()
with c3:
    st.subheader("Follow-up")
    st.write("Post-placement check-ins and escalations.")
    if st.button("Open Follow-up →", key="open_followup"):
        st.session_state["_goto_page"] = "pages/92_Followup_Workflow.py"
        st.experimental_rerun()
