
# 07_Placement_Workflow.py — self-hidden
import streamlit as st
st.set_page_config(page_title="Placement Workflow", page_icon="🏡", layout="wide")
from ui_chrome import hide_pages
hide_pages(["06_Intake_Workflow","07_Placement_Workflow","08_Followup_Workflow","00_Workflows"])

import store, ui_sections as ui
store.init()

lead = store.get_lead(store.get_selected_lead_id()) if store.get_selected_lead_id() else None
st.title("Placement Workflow")
if not lead: st.info("Select a client, then return."); st.stop()
st.caption(f"{lead['name']} • {lead.get('city','')}")

ui.render_financial(lead, ns="main")
ui.render_notifications(lead, ns="main")
