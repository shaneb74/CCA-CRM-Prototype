
# 08_Followup_Workflow.py — guided post-placement follow-up
import streamlit as st
st.set_page_config(page_title="Follow-up Workflow", page_icon="📞", layout="wide")

import store
from ui_chrome import hide_pages
import ui_sections as ui

hide_pages(["06_Intake_Workflow", "07_Placement_Workflow", "08_Followup_Workflow", "00_Workflows"])

store.init()

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Follow-up Workflow")
if not lead:
    st.info("Select a client, then return.")
    st.stop()

st.caption(f"{lead['name']} • {lead['city']}")

steps = ["Check-in", "Satisfaction", "Close"]
step = st.sidebar.radio("Steps", steps, index=0, key=f"follow_steps_{lead_id}")

if step == "Check-in":
    st.text_area("Summary of call", key=f"fu_summary_{lead_id}", height=120)
    ui.render_notifications(lead, ns="main")
elif step == "Satisfaction":
    st.slider("Satisfaction (1=low, 5=high)", 1, 5, value=4, key=f"fu_sat_{lead_id}")
    st.text_area("Concerns / escalations", key=f"fu_escalate_{lead_id}")
else:
    st.checkbox("Close case", key=f"fu_close_{lead_id}")
    if st.button("Save & Close"):
        ui.save_from_session(lead_id)

st.divider()
with st.expander("Data drawers", expanded=False):
    tabs = st.tabs(["Placement", "Documents"])
    with tabs[0]: ui.render_placement(lead, ns="drawer")
    with tabs[1]: ui.render_documents(lead, ns="drawer")
