# pages/08_Followup_Workflow.py — minimal guided follow-up (self-hidden)
import streamlit as st
st.set_page_config(page_title="Follow-up Workflow", page_icon="📞", layout="wide")
from ui_chrome import hide_default; hide_default()
import store, ui_sections as ui; store.init()
lead = store.get_lead(store.get_selected_lead_id()) if store.get_selected_lead_id() else None
st.title("Follow-up Workflow")
if not lead: st.info("Select a client, then return."); st.stop()
st.caption(f"{lead['name']} • {lead.get('city','')}")
ui.notes(lead, ns="main")