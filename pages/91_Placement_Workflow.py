from ui_chrome import apply_chrome
apply_chrome()

import streamlit as st, store
store.init()
st.title("Placement Workflow")

lead = store.get_lead(store.get_selected_lead_id()) if store.get_selected_lead_id() else None
if not lead:
    st.info("Select a client, then return.")
    st.stop()

st.caption(f"{lead.get('name','')} • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")
st.write("Shortlist communities, schedule tours, capture outcomes. (Prototype shell)")

if st.button("← Back to Workflows"):
    st.session_state["_goto_page"]="pages/89_Workflows.py"
    st.experimental_rerun()
