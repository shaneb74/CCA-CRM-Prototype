
# 00_Workflows.py — hub to launch guided workflows, with selected client context
import streamlit as st
import store

store.init()

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
    st.button("Open Intake", key="wf_intake",
              on_click=lambda: st.session_state.update(intake_lead_id=lead['id']),
              disabled=not mine, help=None if mine else "Only assigned advisor can run intake.")
    if hasattr(st, "page_link"):
        st.page_link("pages/06_Intake_Workflow.py", label="Go →")
with c2:
    st.header("Placement")
    st.write("Shortlist communities, schedule tours, record outcomes.")
    if hasattr(st, "page_link"):
        st.page_link("pages/07_Placement_Workflow.py", label="Go →")
with c3:
    st.header("Follow-up")
    st.write("Post-placement check-ins and escalations.")
    if hasattr(st, "page_link"):
        st.page_link("pages/08_Followup_Workflow.py", label="Go →")
