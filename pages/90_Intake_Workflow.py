
# pages/90_Intake_Workflow.py
import streamlit as st
import store
from ui_chrome import apply_chrome
apply_chrome()  # idempotent

# Keep layout simple; do not alter app-wide styling
store.init()

st.title("Intake Workflow")

lead_id = store.get_selected_lead_id()
if not lead_id:
    st.info("Select a client in Client Record first.")
    st.stop()

lead = store.get_lead(lead_id)

# Header (kept minimal to avoid design drift)
st.caption(f"{lead.get('name','—')} • {lead.get('city','—')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

# Basic intake fields (non-destructive placeholders)
with st.container(border=True):
    st.subheader("Client Details")
    st.text_input("Full name", value=lead.get("name",""), key="intake_name")
    st.text_input("Status", value=str(lead.get("status","")).title(), key="intake_status")
    st.number_input("Budget / mo", value=int(lead.get("budget",0) or 0), step=100, key="intake_budget")
    st.text_area("Notes", value=lead.get("notes",""), key="intake_notes", height=120)

# Completion -> marks intake as done and navigates to Placement
if st.button("Complete Intake → Start Placement", type="primary", key="intake_complete_btn"):
    if lead and lead.get("id"):
        # update minimal fields if changed (demo-friendly)
        lead["name"] = st.session_state.get("intake_name", lead["name"])
        lead["notes"] = st.session_state.get("intake_notes", lead.get("notes"))
        try:
            lead["budget"] = int(st.session_state.get("intake_budget", lead.get("budget", 0)) or 0)
        except Exception:
            pass
        lead["intake_completed"] = True
        store.upsert_lead(lead)

    st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
    st.rerun()

# Back affordance (optional)
if st.button("◀ Back to Workflows", key="back_to_wf"):
    st.session_state["_goto_page"] = "pages/89_Workflows.py"
    st.rerun()