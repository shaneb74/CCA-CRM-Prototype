
# pages/90_Intake_Workflow.py
# Intake workflow page using Workflows/Intake/progress helpers

from __future__ import annotations
import streamlit as st
import datetime as dt

# optional chrome (safe if missing)
try:
    from ui_chrome import apply_chrome as _apply_chrome
    _apply_chrome()
except Exception:
    pass

import store
from Workflows.Intake import progress as ip

st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
store.init()

# guard: need a selected lead
lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")

if not lead:
    st.info("Select a client in Client Record first.")
    st.stop()

# --- client context summary (compact) ---
ip.show_intake_summary(lead)

# --- progress header with spacing ---
ip.show_intake_progress(lead)

# --------- Milestone sections ----------
# 01 Lead assigned (simple toggle for prototype)
with st.expander("Lead assigned", expanded=False):
    assigned = lead.get("assigned_to")
    st.write(f"Assigned to: **{assigned or 'Unassigned'}**")
    auto_assign = st.checkbox("Mark as assigned to me", value=False, key="intake_mark_assigned")
    if auto_assign:
        me = getattr(store, "CURRENT_USER", "Current Advisor")
        if assigned != me:
            lead["assigned_to"] = me
            store.upsert_lead(lead)
            ip.set_status(lead["id"], "lead_assigned", True)
            st.success(f"Assigned to {me}")
            st.experimental_rerun()

# 02 Initial contact attempted (data-backed example)
with st.expander("Initial contact attempted", expanded=False):
    c1, c2 = st.columns([1,2])
    with c1:
        when = st.datetime_input("When", value=dt.datetime.now(), key="ica_when")
        channel = st.selectbox("Channel", ["Phone", "Email", "SMS", "In person"], key="ica_channel")
    with c2:
        notes = st.text_area("Notes", height=96, key="ica_notes", placeholder="Voicemail, spoke with daughter, etc.")
    if st.button("Save attempt", key="save_attempt_btn"):
        ip.log_contact_attempt(lead["id"], when, channel, notes)
        st.success("Logged contact attempt and marked milestone complete.")
        st.experimental_rerun()

    attempts = ip.get_data(lead["id"]).get("contact_attempts", [])
    if attempts:
        st.caption("Recent attempts")
        for a in reversed(attempts[-5:]):
            st.write(f"- {a['ts']} • {a['channel']} — {a.get('notes','')}")

# 03 Initial contact made (placeholder for now)
with st.expander("Initial contact made", expanded=False):
    st.caption("Prototype placeholder")
    st.write("Capture who you spoke with and summary; save will mark milestone complete.")

# 04 Consultation scheduled (placeholder)
with st.expander("Consultation scheduled", expanded=False):
    st.caption("Prototype placeholder")
    st.write("Add a date/time and location/Zoom; saving would mark milestone complete.")

# 05 Assessment started (placeholder)
with st.expander("Assessment started", expanded=False):
    st.caption("Prototype placeholder")
    st.write("Starting Care Planner + Cost Calculator can set this automatically.")

# 06 Assessment completed (placeholder)
with st.expander("Assessment completed", expanded=False):
    st.caption("Prototype placeholder")
    st.write("Require key sections complete before marking done.")

# 07 Qualification decision (placeholder)
with st.expander("Qualification decision", expanded=False):
    st.caption("Prototype placeholder")
    st.write("Qualified, Deferred, or Declined with reason codes.")

st.markdown("---")
c1, c2 = st.columns([1,1])
with c1:
    if st.button("Complete Intake → Start Placement", type="primary"):
        ip.set_status(lead["id"], "assessment_completed", True)
        ip.set_status(lead["id"], "qualified_decision", True)
        # schedule redirect
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.experimental_rerun()
with c2:
    st.link_button("↩︎ Back to Workflows", "pages/89_Workflows.py")
