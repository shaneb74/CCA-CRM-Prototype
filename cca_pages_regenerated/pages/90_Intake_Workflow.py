from ui_chrome import apply_chrome
apply_chrome()

import streamlit as st, store
store.init()
st.title("Intake Workflow")

lead = store.get_lead(store.get_selected_lead_id()) if store.get_selected_lead_id() else None
if not lead:
    st.info("No client selected. Use Client Record or the Workflows hub.")
    st.stop()

st.caption(f"{lead.get('name','')} • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

c1,c2,c3 = st.columns(3)
c1.text_input("Full name", value=lead.get("name",""), key="intake_name", label_visibility="visible")
c2.selectbox("Status", ["new","in_progress","hold","closed"], index=0, key="intake_status")
c3.number_input("Budget / mo", value=float(lead.get('budget',0) or 0), step=100.0, key="intake_budget")

if st.button("← Back to Workflows"):
    st.session_state["_goto_page"]="pages/89_Workflows.py"
    st.experimental_rerun()
