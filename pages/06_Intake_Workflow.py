
# 06_Intake_Workflow.py — guided process that pulls in data compartments
import streamlit as st
import store
import ui_sections as ui

store.init()

lead_id = st.session_state.get("intake_lead_id") or store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None
if not lead:
    st.info("No client selected. Use the Workflows hub or Client Record to choose one.")
    st.stop()

st.title("Intake Workflow")
st.caption(f"{lead['name']} • {lead['city']} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

# Guard: only assigned advisor can run intake
mine = ((lead.get("assigned_to") or "").strip().lower()
        == (store.CURRENT_USER or "").strip().lower())
if not mine:
    st.error("Only the assigned advisor can run intake for this client.")
    st.stop()

# Steps
steps = ["Contact", "Care needs", "Financial", "Lifestyle", "Summary"]
step = st.sidebar.radio("Steps", steps, index=0, key=f"intake_steps_{lead_id}")

if step == "Contact":
    ui.render_personal(lead)
elif step == "Care needs":
    ui.render_medical(lead)
elif step == "Financial":
    ui.render_financial(lead)
elif step == "Lifestyle":
    ui.render_lifestyle(lead)
else:
    st.success("Summary")
    st.write("Review and save changes.")
    if st.button("Save"):
        ui.save_from_session(lead_id)

st.divider()
with st.expander("Data drawers (quick access)", expanded=False):
    tabs = st.tabs(["Personal", "Housing", "Medical", "Financial", "Lifestyle", "Placement", "Documents"])
    with tabs[0]: ui.render_personal(lead)
    with tabs[1]: ui.render_housing(lead)
    with tabs[2]: ui.render_medical(lead)
    with tabs[3]: ui.render_financial(lead)
    with tabs[4]: ui.render_lifestyle(lead)
    with tabs[5]: ui.render_placement(lead)
    with tabs[6]: ui.render_documents(lead)
