
# pages/90_Intake_Workflow.py
# Intake Workflow — horizontal stage chips with active highlight + auto-open drawer

from __future__ import annotations
import datetime as _dt
import streamlit as st

# Optional chrome; safe if not present
try:
    from ui_chrome import apply_chrome  # type: ignore
    apply_chrome()
except Exception:
    pass

import store

# ---------- helpers ----------

STEPS = [
    ("lead_received", "Lead received"),
    ("lead_assigned", "Lead assigned"),
    ("initial_attempt", "Initial contact attempted"),
    ("initial_contact", "Initial contact made"),
    ("consultation", "Consultation scheduled"),
    ("assessment_started", "Assessment started"),
    ("assessment_completed", "Assessment completed"),
    ("qualified", "Qualification decision"),
]

def _get_case_steps(lead_id: str) -> dict:
    """Return step dict with safe defaults (all False)."""
    steps = st.session_state.get("case_steps", {}).get(lead_id, {})
    # fill any missing keys
    base = {k: bool(steps.get(k, False)) for k, _ in STEPS}
    return base

def _active_key(steps: dict) -> str:
    """Return the *current* step key: the first False after trailing Trues.
    If all False -> first key. If all True -> last key.
    """
    # position is count of consecutive True from start
    pos = 0
    for k, _ in STEPS:
        if steps.get(k):
            pos += 1
        else:
            break
    if pos >= len(STEPS):
        pos = len(STEPS) - 1
    return STEPS[pos][0]

def _chip_row(steps: dict, active: str):
    # CSS for rectangular chips laid out horizontally
    st.markdown(
        """
        <style>
        .chip-row{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0 6px 0;}
        .chip{
            padding:8px 14px;border:1px solid #e5e7eb;border-radius:8px;
            background:#fff;color:#111827;font-size:13px;line-height:1;
            box-shadow:0 1px 0 rgba(0,0,0,.02);
            opacity:.8;
        }
        .chip.active{
            border-color:#2563eb;background:#eff6ff;color:#1d4ed8;
            opacity:1;font-weight:600;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="chip-row">' + "".join(
        f'<div class="chip {"active" if k==active else ""}">{lbl}</div>'
        for k, lbl in STEPS
    ) + "</div>", unsafe_allow_html=True)

def _case_snapshot(lead: dict):
    st.markdown("### Case snapshot")
    st.caption(f"{lead.get('name','')} • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")
    st.write(f"**Care preference:** {lead.get('preference','—')}")
    budget = lead.get("budget")
    st.write(f"**Budget:** ${int(budget):,}/mo" if isinstance(budget,(int,float)) and budget>0 else "**Budget:** —")
    st.write(f"**Timeline:** {lead.get('timeline','—')}")
    if lead.get("notes"):
        st.write(f"**Notes:** {lead.get('notes')}")

def _sla_banner(lead: dict, active_key: str):
    """Very light SLA indicator using the lead's created time if available."""
    received = st.session_state.get("_lead_received_at")
    if not received:
        received = _dt.datetime.utcnow()
        st.session_state["_lead_received_at"] = received
    # target windows per step (in hours) – demo only
    SLA_HOURS = {
        "lead_received": 0,
        "lead_assigned": 24,
        "initial_attempt": 2,
        "initial_contact": 48,
        "consultation": 72,
        "assessment_started": 72,
        "assessment_completed": 120,
        "qualified": 24,
    }
    # rough due time from "received"
    elapsed = _dt.datetime.utcnow() - received
    base_hours = sum(SLA_HOURS[k] for k,_ in STEPS if k==active_key or not SLA_HOURS.get(k) and False)
    # ^ in this demo we just use the SLA of the active step
    due = received + _dt.timedelta(hours=SLA_HOURS.get(active_key, 24))
    remaining = (due - _dt.datetime.utcnow())
    state = "On track ✅" if remaining.total_seconds() > 0 else "Overdue ⚠️"
    st.caption(f"**Next action:** {dict(STEPS)[active_key]} • {state} • **Due:** {due.strftime('%Y-%m-%d %H:%M UTC')}")

# ---------- page ----------

st.set_page_config(page_title="Intake Workflow", page_icon="📋", layout="wide")
store.init()

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")
if not lead:
    st.info("Select a client in Client Record first.")
    st.stop()

# Header inline facts
hc1, hc2, hc3, hc4 = st.columns([2,1,1,1])
with hc1:
    st.markdown(f"**{lead.get('name','')}** • {lead.get('city','')}")
    st.caption(f"Assigned: {lead.get('assigned_to') or 'Unassigned'}")
with hc2:
    st.caption("Status")
    st.write(str(lead.get('status','')).replace('_',' '))
with hc3:
    st.caption("Budget / mo")
    budget = lead.get("budget")
    st.write(f"${int(budget):,}" if isinstance(budget,(int,float)) and budget>0 else "—")
with hc4:
    st.caption("Timeline")
    st.write(lead.get("timeline","—"))

# Origin + received chips row
oc1, oc2 = st.columns([1,1])
with oc1:
    st.button(f"Origin: {str(lead.get('origin','app')).lower()}", disabled=True)
with oc2:
    st.button("Received: 0s ago", disabled=True)

# Horizontal status chips
steps = _get_case_steps(lead_id)
active = _active_key(steps)
_chip_row(steps, active)

# SLA banner
_sla_banner(lead, active)

st.progress(min(0.99, (list(dict(STEPS).keys()).index(active)+1)/len(STEPS)))

# Auto-open the active drawer on first load
st.session_state.setdefault("intake_active_open_key", active)
open_key = st.session_state.get("intake_active_open_key", active)

# Two-column layout: drawers (left) + snapshot (right)
lc, rc = st.columns([2,1])

with lc:
    for key, label in STEPS:
        with st.expander(label, expanded=(key==open_key)):
            st.write("Checklist / fields for:", label)
            # Example checklist boxes (they also flip step state for demo)
            done = st.checkbox("Mark complete", value=bool(steps.get(key, False)), key=f"chk_{key}")
            if done != steps.get(key, False):
                # Update session steps
                all_steps = st.session_state.setdefault("case_steps", {})
                one = all_steps.setdefault(lead_id, {})
                one[key] = done
                st.session_state["case_steps"] = all_steps
                # if you mark this step complete and there is a next step, auto-advance open drawer
                if done:
                    keys = [k for k,_ in STEPS]
                    idx = keys.index(key)
                    if idx < len(keys)-1:
                        st.session_state["intake_active_open_key"] = keys[idx+1]
                st.experimental_rerun()

with rc:
    _case_snapshot(lead)

st.button("Complete Intake → Start Placement", key="btn_finish")
st.link_button("← Back to Workflows", "pages/89_Workflows.py")
