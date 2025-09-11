# pages/90_Intake_Workflow.py
import streamlit as st
import store

st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
store.init()

# --- Compact header with client context ---
lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")
if not lead:
    st.info("Select a client in Client Record first.")
    st.stop()

name = lead.get('name',''); city = lead.get('city',''); assigned = lead.get('assigned_to') or 'Unassigned'
st.caption(f"{name} • {city} • Assigned: {assigned}")

# summary grid (non-editing)
g1,g2,g3,g4 = st.columns([1,1,1,3])
with g1: st.caption("Status"); st.write(lead.get('status','New'))
with g2: st.caption("Budget / mo"); st.write(lead.get('budget','—'))
with g3: st.caption("Timeline"); st.write(lead.get('timeline','—'))
with g4:
    if lead.get('notes'):
        st.caption("Notes"); st.write(lead.get('notes'))

st.divider()

from Workflows.Intake.progress import show_intake_progress, ensure_css_spacing

ensure_css_spacing()
show_intake_progress(lead_id)

# Actions
a1,a2 = st.columns([2,1])
with a1:
    if st.button("Complete Intake → Start Placement", type="primary", key="complete_intake_then_place"):
        # mark final milestone and set redirect for next run
        st.session_state.setdefault('intake_status',{}).setdefault(lead_id,{})
        st.session_state['intake_status'][lead_id]['qualified_decision'] = True
        st.session_state['_goto_page'] = "pages/91_Placement_Workflow.py"
        st.rerun()

with a2:
    if st.button("← Back to Workflows", key="back_to_workflows"):
        st.session_state['_goto_page'] = "pages/89_Workflows.py"
        st.rerun()