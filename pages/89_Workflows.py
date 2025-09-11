# pages/89_Workflows.py
import streamlit as st
try:
    import store
except Exception:
    store=None
try:
    st.set_page_config(page_title="Workflows", page_icon="🗂️", layout="wide")
except Exception: pass
if store:
    try: store.init()
    except Exception: pass
st.title("Workflows")
lead_id=None; lead=None
if store:
    try:
        lead_id=store.get_selected_lead_id(); lead=store.get_lead(lead_id) if lead_id else None
    except Exception: pass
if not lead:
    st.info("Select a client in Client Record first."); st.stop()
st.caption(f"Client: **{lead.get('name','')}** ({lead.get('id','')}) · {lead.get('city','')} · Assigned: {lead.get('assigned_to') or '—'}")
c1,c2,c3=st.columns(3)
with c1:
    st.subheader("Intake"); st.write("Collect personal, care, financial, lifestyle.")
    if st.button("Open Intake →", key="open_intake"):
        try:
            if store: store.set_selected_lead(lead.get("id"))
            if hasattr(st,"switch_page"): st.switch_page("pages/90_Intake_Workflow.py")
            else: st.session_state["_goto_page"]="pages/90_Intake_Workflow.py"; st.experimental_rerun()
        except Exception:
            st.session_state["_goto_page"]="pages/90_Intake_Workflow.py"; st.experimental_rerun()
with c2:
    st.subheader("Placement"); st.write("Shortlist communities, schedule tours, record outcomes.")
    if st.button("Open Placement →", key="open_placement_from_hub"):
        st.session_state["_goto_page"]="pages/91_Placement_Workflow.py"; st.experimental_rerun()
with c3:
    st.subheader("Follow-up"); st.write("Post-placement check-ins and escalations.")
    if st.button("Open Follow-up →", key="open_followup_from_hub"):
        st.session_state["_goto_page"]="pages/92_Followup_Workflow.py"; st.experimental_rerun()
