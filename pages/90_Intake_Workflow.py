
# pages/90_Intake_Workflow.py
# Intake workflow: two-column layout with SLA indicator and case snapshot
from __future__ import annotations
import streamlit as st
import datetime as dt
import store

def _consume_redirect_once():
    dest = st.session_state.pop("_goto_page", None)
    if dest and hasattr(st, "switch_page"):
        try:
            st.switch_page(dest)
        except Exception:
            pass

st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
_consume_redirect_once()
store.init()

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None
if not lead:
    st.info("Select a client in Client Record first.")
    st.stop()

# ---- intake state scaffolding ----
steps = [
    "Lead received",
    "Lead assigned",
    "Initial contact attempted",
    "Initial contact made",
    "Consultation scheduled",
    "Assessment started",
    "Assessment completed",
    "Qualification decision",
]
# SLA windows (hours) for next-step due
SLA_HOURS = {
    "Lead received": 0,
    "Lead assigned": 8,
    "Initial contact attempted": 2,
    "Initial contact made": 24,
    "Consultation scheduled": 48,
    "Assessment started": 72,
    "Assessment completed": 120,
    "Qualification decision": 24,
}

key = f"intake_state::{lead_id}"
state = st.session_state.get(key)
if not state:
    state = {
        "done": {s: False for s in steps},
        "ts": {"Lead received": dt.datetime.now()},
    }
    st.session_state[key] = state

done = state["done"]; ts = state["ts"]

def _next_step_and_due():
    for s in steps:
        if not done.get(s, False):
            prev_index = steps.index(s) - 1
            if prev_index >= 0:
                prev = steps[prev_index]
                base = ts.get(prev) or ts.get("Lead received") or dt.datetime.now()
            else:
                base = ts.get("Lead received") or dt.datetime.now()
            due = base + dt.timedelta(hours=SLA_HOURS.get(s, 0))
            return s, due
    return "All steps complete", dt.datetime.now()

next_step, due_at = _next_step_and_due()
now = dt.datetime.now()
remaining = due_at - now
remaining_h = int(remaining.total_seconds() // 3600)

def _status_badge():
    if "complete" in next_step.lower():
        color = "#10b981"; text = "All steps complete"
    else:
        if remaining.total_seconds() < 0:
            color = "#ef4444"; text = f"Overdue • {abs(remaining_h)}h"
        elif remaining.total_seconds() < 6*3600:
            color = "#f59e0b"; text = f"Due soon • {remaining_h}h"
        else:
            color = "#3b82f6"; text = f"Due in {remaining_h}h"
    st.markdown(f"""
    <div style="display:flex; gap:10px; align-items:center; margin:6px 0 14px 0;">
      <span style="font-weight:600;">Next action:</span>
      <span style="padding:4px 10px; border-radius:999px; background:#f3f4f6;">{next_step}</span>
      <span style="padding:4px 10px; border-radius:999px; color:white; background:{color};">{text}</span>
    </div>
    """, unsafe_allow_html=True)

# Pills row (unchanged, horizontal)
st.subheader("Intake progress")
pct = int(100 * sum(1 for s in steps if done.get(s)) / len(steps))
st.progress(pct/100.0)

pill_css = """
<style>
.pill { display:inline-block; padding:6px 12px; border-radius:999px; background:#f3f4f6; margin:6px 8px 12px 0; font-size:12px; }
.pill.done { background:#e0f2f1; color:#065f46; }
</style>
"""
st.markdown(pill_css, unsafe_allow_html=True)
row = ""
for s in steps:
    cls = "pill done" if done.get(s) else "pill"
    row += f'<span class="{cls}">{s}</span>'
st.markdown(row, unsafe_allow_html=True)

_status_badge()

left, right = st.columns([1.1, 0.9])

with left:
    for s in steps:
        with st.expander(s, expanded=False):
            if st.checkbox(f"Mark '{s}' done", value=done.get(s, False), key=f"chk::{s}"):
                if not done.get(s):
                    done[s] = True
                    ts[s] = dt.datetime.now()
                    st.session_state[key] = {"done": done, "ts": ts}
                    st.experimental_rerun()

with right:
    st.subheader(lead.get("name",""))
    st.caption(f"{lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")
    with st.container(border=True):
        c1,c2 = st.columns(2)
        with c1:
            st.caption("Status"); st.write(lead.get("status","New"))
            st.caption("Timeline"); st.write(lead.get("timeline","—"))
        with c2:
            st.caption("Budget / mo")
            budget = lead.get("budget", 0)
            st.write('${:,}'.format(int(budget)) if budget else "—")
            st.caption("Lead ID"); st.write(lead.get("id","—"))
        st.markdown("---")
        st.caption("Notes")
        st.write(lead.get("notes") or "—")
    st.text_area("Quick note", key=f"note::{lead_id}", placeholder="Add a quick note…")

st.divider()
c1, c2 = st.columns([1,1])
with c1:
    if st.button("Complete Intake → Start Placement", type="primary"):
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.experimental_rerun()
with c2:
    if st.button("← Back to Workflows"):
        st.session_state["_goto_page"] = "pages/89_Workflows.py"
        st.experimental_rerun()
