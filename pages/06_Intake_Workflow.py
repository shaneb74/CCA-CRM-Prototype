
# 06_Intake_Workflow.py — guided intake (self-hidden)
import streamlit as st
st.set_page_config(page_title="Intake Workflow", page_icon="📝", layout="wide")

import store
from ui_chrome import hide_pages
import ui_sections as ui

# Hide guided pages + hub from sidebar
hide_pages(["06_Intake_Workflow", "07_Placement_Workflow", "08_Followup_Workflow", "00_Workflows"])

store.init()

lead_id = st.session_state.get("intake_lead_id") or store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None
if not lead:
    st.info("No client selected. Use the Workflows hub or Client Record to choose one.")
    st.stop()

st.title("Intake Workflow")
st.caption(f"{lead['name']} • {lead['city']} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

mine = ((lead.get("assigned_to") or "").strip().lower() == (store.CURRENT_USER or "").strip().lower())
if not mine:
    st.error("Only the assigned advisor can run intake for this client.")
    st.stop()

steps = ["Contact", "Care needs", "Financial", "Lifestyle", "Summary"]
step = st.sidebar.radio("Steps", steps, index=0, key=f"intake_steps_{lead_id}")

if step == "Contact":
    ui.render_personal(lead, ns="main")
elif step == "Care needs":
    ui.render_medical(lead, ns="main")
elif step == "Financial":
    ui.render_financial(lead, ns="main")
elif step == "Lifestyle":
    ui.render_lifestyle(lead, ns="main")
else:
    st.success("Summary")
    st.write("Review and save changes.")
    if st.button("Save"):
        ui.save_from_session(lead_id)

st.divider()
with st.expander("Data drawers (quick access)", expanded=False):
    tabs = st.tabs(["Personal", "Housing", "Medical", "Financial", "Lifestyle", "Placement", "Documents"])
    with tabs[0]: ui.render_personal(lead, ns="drawer")
    with tabs[1]: ui.render_housing(lead, ns="drawer")
    with tabs[2]: ui.render_medical(lead, ns="drawer")
    with tabs[3]: ui.render_financial(lead, ns="drawer")
    with tabs[4]: ui.render_lifestyle(lead, ns="drawer")
    with tabs[5]: ui.render_placement(lead, ns="drawer")
    with tabs[6]: ui.render_documents(lead, ns="drawer")
