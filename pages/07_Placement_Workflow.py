
# 07_Placement_Workflow.py — guided placement (self-hidden)
import streamlit as st
st.set_page_config(page_title="Placement Workflow", page_icon="🏡", layout="wide")

import store
from ui_chrome import hide_pages
import ui_sections as ui

hide_pages(["06_Intake_Workflow", "07_Placement_Workflow", "08_Followup_Workflow", "00_Workflows"])

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
    ui.render_housing(lead, ns="main")
    ui.render_financial(lead, ns="main")
    ui.render_placement(lead, ns="main")
elif step == "Tours":
    ui.render_placement(lead, ns="main")
elif step == "Decision":
    st.selectbox("Outcome", ["Pending","Accepted","Declined"], key=f"place_outcome_{lead_id}")
    st.text_area("Notes", key=f"place_decision_notes_{lead_id}", height=120)
    if st.button("Save decision"):
        ui.save_from_session(lead_id)

st.divider()
with st.expander("Data drawers", expanded=False):
    tabs = st.tabs(["Personal", "Medical", "Documents"])
    with tabs[0]: ui.render_personal(lead, ns="drawer")
    with tabs[1]: ui.render_medical(lead, ns="drawer")
    with tabs[2]: ui.render_documents(lead, ns="drawer")
