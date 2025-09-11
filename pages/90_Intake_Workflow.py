
# pages/90_Intake_Workflow.py
from __future__ import annotations
import streamlit as st
from datetime import date, datetime
import math

# Safe imports
try:
    import store
except Exception:
    store = None

# Local UI helpers for pills/progress
try:
    from Workflows.Intake.progress import render_pills, progress_fraction, first_incomplete_index
except Exception:
    # Fallback no-op to keep page from crashing if path differs
    def render_pills(steps): 
        st.write("Intake steps:", ", ".join(s.get("label","") for s in steps))
    def progress_fraction(steps): 
        return 0.0
    def first_incomplete_index(steps): 
        return 0

# --- Page config (guard against duplicates) ---
_once = "_cca_intake_pgconf"
if not st.session_state.get(_once):
    try:
        st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
    except Exception:
        pass
    st.session_state[_once] = True

def _lead():
    lead_id = None
    if store:
        lead_id = getattr(store, "get_selected_lead_id", lambda: None)()
    if store and lead_id:
        return store.get_lead(lead_id)
    return None

def _seed_steps(lead) -> list[dict]:
    # Build standard steps. In a real app these would be persisted.
    def step(label, key):
        # attach persisted booleans if they exist in session
        val = st.session_state.get(f"intake_{key}_{lead.get('id','')}", False)
        return {
            "label": label,
            "key": key,
            "completed": bool(val),
            "sla_due": None,  # could be dates if you have them
        }
    return [
        step("Lead received", "lead_received"),
        step("Lead assigned", "lead_assigned"),
        step("Initial contact attempted", "initial_attempt"),
        step("Initial contact made", "contact_made"),
        step("Consultation scheduled", "consult_scheduled"),
        step("Assessment started", "assessment_started"),
        step("Assessment completed", "assessment_completed"),
        step("Qualification decision", "qualified"),
    ]

lead = _lead()
if not lead:
    st.info("No client selected. Use **Client Record** to pick a client, then return.")
    st.stop()

# Sticky case summary
st.title("Intake Workflow")
sub = f"{lead.get('name','')} • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}"
st.caption(sub)

c1, c2, c3, c4 = st.columns([1,1,1,1])
with c1:
    st.caption("Status")
    st.write(str(lead.get("status","")).replace("_"," ").title() or "—")
with c2:
    st.caption("Budget / mo")
    budget = lead.get("budget", 0) or 0
    st.metric(label="", value=f"{int(budget):,}" if budget else "—")
with c3:
    st.caption("Timeline")
    st.write(lead.get("timeline","—"))
with c4:
    st.caption("Notes")
    st.write(lead.get("notes") or "—")

st.divider()

# Steps + progress
steps = _seed_steps(lead)
pct = progress_fraction(steps)
st.caption("Intake progress")
st.progress(min(max(pct,0.0),1.0))
render_pills(steps)

st.markdown(" ")  # breathing room

# Grouped sections
st.subheader("Contact & Scheduling", anchor=False)
with st.expander("Lead received", expanded=False):
    st.checkbox("Mark lead received", key=f"intake_lead_received_{lead.get('id','')}")
with st.expander("Lead assigned", expanded=False):
    st.checkbox("Mark lead assigned", key=f"intake_lead_assigned_{lead.get('id','')}")
with st.expander("Initial contact attempted", expanded=False):
    st.selectbox("Contact method", ["Phone","Email","SMS","Other"], key=f"intake_attempt_method_{lead.get('id','')}")
    st.text_area("Notes", key=f"intake_attempt_notes_{lead.get('id','')}")
    st.checkbox("Mark initial attempt complete", key=f"intake_initial_attempt_{lead.get('id','')}")
with st.expander("Initial contact made", expanded=False):
    st.date_input("Date contacted", key=f"intake_contact_date_{lead.get('id','')}", value=date.today())
    st.text_area("Summary / outcome", key=f"intake_contact_notes_{lead.get('id','')}")
    st.checkbox("Mark contact made", key=f"intake_contact_made_{lead.get('id','')}")
with st.expander("Consultation scheduled", expanded=False):
    st.date_input("Consultation date", key=f"intake_consult_dt_{lead.get('id','')}", value=date.today())
    st.time_input("Consultation time", key=f"intake_consult_time_{lead.get('id','')}")
    st.checkbox("Mark consultation scheduled", key=f"intake_consult_scheduled_{lead.get('id','')}")

st.subheader("Assessment", anchor=False)
with st.expander("Assessment started", expanded=False):
    st.text_input("Who provided information", placeholder="Resident, Daughter, POA, etc.", key=f"intake_assessor_{lead.get('id','')}")
    st.checkbox("Mark assessment started", key=f"intake_assessment_started_{lead.get('id','')}")
with st.expander("Assessment completed", expanded=False):
    st.text_area("Assessment notes", key=f"intake_assess_notes_{lead.get('id','')}")
    st.checkbox("Mark assessment completed", key=f"intake_assessment_completed_{lead.get('id','')}")

st.subheader("Decision", anchor=False)
with st.expander("Qualification decision", expanded=False):
    st.selectbox("Outcome", ["Qualified","Deferred","Declined"], key=f"intake_qualified_outcome_{lead.get('id','')}")
    st.text_area("Reason / comments", key=f"intake_qualified_reason_{lead.get('id','')}")
    st.checkbox("Mark decision recorded", key=f"intake_qualified_{lead.get('id','')}")

st.markdown("")
cols = st.columns([2,1])
with cols[0]:
    disabled = not all(s.get("completed") for s in _seed_steps(lead))
    if st.button("Complete Intake → Start Placement", type="primary", disabled=disabled):
        # Persist a simple flag in session to indicate 'intake complete'
        st.session_state[f"intake_done_{lead.get('id','')}"] = True
        # redirect (safe, no rerun inside callback)
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.experimental_rerun()
with cols[1]:
    if st.button("← Back to Workflows"):
        st.session_state["_goto_page"] = "pages/89_Workflows.py"
        st.experimental_rerun()
