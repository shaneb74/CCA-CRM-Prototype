import streamlit as st
import store

try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    pass

st.set_page_config(page_title="Intake Workflow", page_icon="📝", layout="wide")
store.init()

lead_id = store.get_selected_lead_id()
if not lead_id:
    st.info("Select a client in Client Record first.")
    st.stop()
lead = store.get_lead(lead_id)

st.title("Intake Workflow")
st.caption(f"{lead.get('name','—')} • {lead.get('city','—')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

try:
    from Workflows.Intake.intake_sla import log_stage
    log_stage(lead, "assessment_started", meta={"by": lead.get("assigned_to") or "advisor"})
    store.upsert_lead(lead)
except Exception:
    pass

with st.container(border=True):
    st.subheader("Client Details")
    name = st.text_input("Full name", value=lead.get("name",""))
    notes = st.text_area("Notes", value=lead.get("notes",""), height=120)
    budget = st.number_input("Budget / mo", value=int(lead.get("budget",0) or 0), step=100)

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Save Intake"):
        lead["name"] = name
        lead["notes"] = notes
        try:
            lead["budget"] = int(budget)
        except Exception:
            pass
        store.upsert_lead(lead)
        st.success("Saved.")
with col2:
    if st.button("Complete Intake → Start Placement", type="primary"):
        try:
            from Workflows.Intake.intake_sla import log_stage
            log_stage(lead, "assessment_completed")
            log_stage(lead, "qualification_decision", meta={"decision": "Qualified"})
        except Exception:
            pass
        lead["intake_completed"] = True
        store.upsert_lead(lead)
        try:
            st.switch_page("pages/91_Placement_Workflow.py")
        except Exception:
            st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
            st.rerun()
