
# 07_Placement_Workflow.py — guided placement process
import streamlit as st
import store
import ui_sections as ui

store.init()

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Placement Workflow")
if not lead:
    st.info("Select a client, then return.")
    st.stop()

st.caption(f"{lead['name']} • {lead['city']}")

steps = ["Shortlist", "Tours", "Decision"]
step = st.sidebar.radio("Steps", steps, index=0, key=f"place_steps_{lead_id}")

if step == "Shortlist":
    ui.render_housing(lead)
    ui.render_financial(lead)
    ui.render_placement(lead)
elif step == "Tours":
    ui.render_placement(lead)
elif step == "Decision":
    st.selectbox("Outcome", ["Pending","Accepted","Declined"], key=f"place_outcome_{lead_id}")
    st.text_area("Notes", key=f"place_decision_notes_{lead_id}", height=120)
    if st.button("Save decision"):
        ui.save_from_session(lead_id)

st.divider()
with st.expander("Data drawers", expanded=False):
    tabs = st.tabs(["Personal", "Medical", "Documents"])
    with tabs[0]: ui.render_personal(lead)
    with tabs[1]: ui.render_medical(lead)
    with tabs[2]: ui.render_documents(lead)
