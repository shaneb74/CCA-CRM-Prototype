# pages/90_Intake_Workflow.py
import streamlit as st
from datetime import datetime, time, date
import store

try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    pass

# Full workflow helpers
try:
    from Workflows.Intake.progress import (
        show_intake_progress, set_step, get_data, log_contact_attempt
    )
except Exception:
    def show_intake_progress(*a, **k): pass
    def set_step(*a, **k): pass
    def get_data(*a, **k): return {}
    def log_contact_attempt(*a, **k): pass

store.init()
lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")
if not lead:
    st.info("No client selected. Use Client Record or the Workflows hub.")
    st.stop()

st.caption(f"{lead.get('name','')} • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

# Top progress
show_intake_progress(lead, title="Intake progress", show_demo_controls=False)

# ---------- Milestone forms (prototype) ----------

# Lead Assigned (auto when supervisor assigns; read-only note here)
with st.expander("Lead assigned", expanded=False):
    st.caption("This milestone is auto-completed when a supervisor assigns the lead to an advisor.")

# Initial Contact Attempted — WORKING FORM
with st.expander("Initial contact attempted", expanded=True):
    st.write("Log at least one attempt to satisfy this milestone.")
    col1, col2 = st.columns([1,1])
    with col1:
        d = st.date_input("Attempt date", value=date.today(), key="ica_date")
        t = st.time_input("Attempt time", value=datetime.now().time().replace(microsecond=0), key="ica_time")
    with col2:
        channel = st.selectbox("Channel", ["Phone", "Email", "SMS", "Other"], key="ica_channel")
        notes = st.text_input("Notes (optional)", key="ica_notes")
    if st.button("Save attempt", type="primary", key="btn_save_attempt"):
        try:
            ts = datetime.combine(d, t)
            log_contact_attempt(lead["id"], ts, channel, notes)
            st.success("Attempt logged. Milestone marked complete.")
        except Exception as e:
            st.error(f"Could not log attempt: {e}")

    # show recent attempts
    try:
        data = get_data(lead["id"])
        attempts = data.get("initial_contact_attempts", [])[-5:]
        if attempts:
            st.write("Recent attempts:")
            for a in reversed(attempts):
                st.write(f"• {a['ts']} — {a['channel']}: {a.get('notes','')}")
        else:
            st.caption("No attempts yet.")
    except Exception:
        pass

# Initial Contact Made — placeholder
with st.expander("Initial contact made", expanded=False):
    st.caption("Prototype placeholder. This will capture successful connection details.")
    disabled = True
    st.text_input("Connected with (name)", disabled=disabled, key="icm_name")
    st.text_area("Call notes", disabled=disabled, key="icm_notes")
    st.button("Mark contact made", disabled=disabled, key="btn_mark_icm")

# Consultation Scheduled — placeholder
with st.expander("Consultation scheduled", expanded=False):
    st.caption("Prototype placeholder. Will capture appointment date/time and participants.")
    st.button("Save consultation", disabled=True)

# Assessment Started — placeholder
with st.expander("Assessment started", expanded=False):
    st.caption("Prototype placeholder. Will record who started which tool and when.")
    st.button("Mark started", disabled=True)

# Assessment Completed — placeholder
with st.expander("Assessment completed", expanded=False):
    st.caption("Prototype placeholder. Will require all sections complete, then allow mark complete.")
    st.button("Mark completed", disabled=True)

# Qualification Decision — placeholder
with st.expander("Qualification decision", expanded=False):
    st.caption("Prototype placeholder. Will capture outcome (Pass/Defer/Decline) and reason.")
    st.button("Save decision", disabled=True)

st.divider()

# Existing primary action stays
if st.button("Complete Intake → Start Placement", type="secondary"):
    if lead and lead.get("id"):
        set_step(lead["id"], "assessment_started", True)
        set_step(lead["id"], "assessment_completed", True)
        set_step(lead["id"], "qualified", True)
        l = store.get_lead(lead["id"])
        if l is not None:
            l["intake_complete"] = True
            store.upsert_lead(l)
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.rerun()

if st.button("↩ Back to Workflows"):
    st.session_state["_goto_page"] = "pages/89_Workflows.py"
    st.rerun()