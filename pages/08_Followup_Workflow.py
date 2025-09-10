
# 08_Followup_Workflow.py — guided post-placement follow-up
import streamlit as st
import store
import ui_sections as ui

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
    ui.render_notifications(lead)
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
    with tabs[0]: ui.render_placement(lead)
    with tabs[1]: ui.render_documents(lead)
