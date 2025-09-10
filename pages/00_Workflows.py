# pages/00_Workflows.py — hidden hub (routable)
import streamlit as st
st.set_page_config(page_title="Workflows", page_icon="🧭", layout="wide")
from ui_chrome import hide_default; hide_default()
import store; store.init()
st.title("Workflows")
lead_id = store.get_selected_lead_id(); lead = store.get_lead(lead_id) if lead_id else None
if not lead: st.info("Select a client in Client Record first."); st.stop()
st.markdown(f"**Client:** {lead['name']} ({lead['id']}) • {lead.get('city','')}  |  Assigned: {lead.get('assigned_to') or 'Unassigned'}")
c1,c2,c3 = st.columns(3)
with c1: st.header("Intake"); st.write("Collect personal, care, financial, lifestyle."); 
st.page_link("pages/06_Intake_Workflow.py", label="Open Intake →") if hasattr(st,"page_link") else None
with c2: st.header("Placement"); st.write("Shortlist, tours, decisions."); 
st.page_link("pages/07_Placement_Workflow.py", label="Open Placement →") if hasattr(st,"page_link") else None
with c3: st.header("Follow-up"); st.write("Post-placement check-ins."); 
st.page_link("pages/08_Followup_Workflow.py", label="Open Follow-up →") if hasattr(st,"page_link") else None