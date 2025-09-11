# pages/90_Intake_Workflow.py
# Minimal-safe Intake page shell that preserves behavior and reliable navigation

import streamlit as st
import store

try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    pass

st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
store.init()

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")
if not lead:
    st.info("No client selected. Use Client Record or the Workflows hub.")
    st.stop()

st.caption(f"{lead.get('name','')} • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

with st.container(border=True):
    st.subheader("Client Details")
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        st.text_input("Full name", value=lead.get("name",""), key="intake_name", label_visibility="visible", disabled=True)
    with c2:
        st.text_input("Status", value=str(lead.get("status","")).replace("_"," ").title(), key="intake_status", disabled=True)
    with c3:
        st.number_input("Budget / mo", value=float(lead.get("budget",0)), step=100.0, key="intake_budget", disabled=True)

    st.text_area("Notes", value=lead.get("notes",""), key="intake_notes", height=120, disabled=True)

# Primary action: mark intake complete and jump to Placement
if st.button("Complete Intake → Start Placement", type="primary"):
    if lead and lead.get("id"):
        # persist the completion flag
        l = store.get_lead(lead["id"])
        if l is not None:
            l["intake_complete"] = True
            store.upsert_lead(l)
        # schedule redirect
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.rerun()

# Back
if st.button("↩ Back to Workflows"):
    st.session_state["_goto_page"] = "pages/89_Workflows.py"
    st.rerun()