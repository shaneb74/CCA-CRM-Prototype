from ui_chrome import apply_chrome, hide_pages
apply_chrome()

import streamlit as st
import store

store.init()

# Hide this page from the sidebar
hide_pages(["88_Workflows_Section"])

st.title("Workflows Hub")
st.caption("Access all client workflow stages from here.")

# Workflow navigation buttons
st.subheader("Available Workflows")
with st.container(border=True):
    st.write("**Intake**: Collect personal, care, financial, and lifestyle details.")
    if st.button("Open Intake Workflow →", key="open_intake"):
        st.session_state["_goto_page"] = "pages/90_Intake_Workflow.py"
        st.rerun()

    st.write("**Placement**: Shortlist communities, schedule tours, and record outcomes.")
    if st.button("Open Placement Workflow →", key="open_placement"):
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.rerun()

    st.write("**Follow-up**: Manage post-placement check-ins and escalations.")
    if st.button("Open Follow-up Workflow →", key="open_followup"):
        st.session_state["_goto_page"] = "pages/92_Followup_Workflow.py"
        st.rerun()

    st.write("**Workflows Overview**: View all workflow stages for a client.")
    if st.button("Open Workflows Overview →", key="open_workflows"):
        st.session_state["_goto_page"] = "pages/89_Workflows.py"
        st.rerun()

# Optional back button to Client Record
if st.button("◀ Back to Client Record", key="back_to_client_record"):
    st.session_state["_goto_page"] = "pages/04_Client_Record.py"
    st.rerun()
