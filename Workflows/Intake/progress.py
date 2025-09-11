
# Workflows/Intake/progress.py
# Data-backed intake progress state + UI helpers

from __future__ import annotations
import datetime as _dt
import streamlit as st

# ---- canonical milestone order ----
MILESTONES = [
    "lead_received",
    "lead_assigned",
    "initial_contact_attempted",
    "initial_contact_made",
    "consultation_scheduled",
    "assessment_started",
    "assessment_completed",
    "qualified_decision",
]

LABELS = {
    "lead_received": "Lead received",
    "lead_assigned": "Lead assigned",
    "initial_contact_attempted": "Initial contact attempted",
    "initial_contact_made": "Initial contact made",
    "consultation_scheduled": "Consultation scheduled",
    "assessment_started": "Assessment started",
    "assessment_completed": "Assessment completed",
    "qualified_decision": "Qualified / decision",
}

def _key(lead_id: str) -> str:
    return f"intake_progress::{lead_id}"

def _ensure_state(lead_id: str):
    k = _key(lead_id)
    if k not in st.session_state:
        st.session_state[k] = {
            "status": {m: False for m in MILESTONES},
            "data": {
                "contact_attempts": [],  # list of dicts
            },
        }
        # When a lead exists in the CRM, treat "received" as complete
        st.session_state[k]["status"]["lead_received"] = True
    return st.session_state[k]

# ---------- actions (data-backed) ----------

def log_contact_attempt(lead_id: str, when: _dt.datetime, channel: str, notes: str = ""):
    s = _ensure_state(lead_id)
    s["data"]["contact_attempts"].append({
        "ts": when.isoformat(),
        "channel": channel,
        "notes": notes.strip(),
    })
    # auto-complete milestone
    s["status"]["initial_contact_attempted"] = True

def set_status(lead_id: str, key: str, value: bool = True):
    s = _ensure_state(lead_id)
    if key in s["status"]:
        s["status"][key] = bool(value)

# ---------- readers ----------
def get_status(lead_id: str) -> dict:
    return _ensure_state(lead_id)["status"]

def get_data(lead_id: str) -> dict:
    return _ensure_state(lead_id)["data"]

def get_progress_pct(lead_id: str) -> float:
    s = get_status(lead_id)
    total = len(MILESTONES)
    done = sum(1 for v in s.values() if v)
    return (done / total) if total else 0.0

# ---------- UI helpers ----------

def _pill(label: str, on: bool):
    base = "background-color:#f3f4f6;color:#6b7280;"
    active = "background-color:#e0f2fe;color:#0369a1;border:1px solid #bae6fd;"
    style = active if on else base
    st.markdown(
        f"""<span style="padding:.20rem .50rem;border-radius:9999px;font-size:12px;{style};margin-right:.35rem;">
        {label}</span>""",
        unsafe_allow_html=True,
    )

def show_intake_progress(lead: dict):
    """
    Renders header pills and a progress bar. Adds a bit of margin below the
    pills so the expanders don't sit directly under them.
    """
    lead_id = lead.get("id","")
    status = get_status(lead_id)

    st.subheader("Intake progress")
    # progress bar
    st.progress(get_progress_pct(lead_id))

    # pill row
    cols = st.columns(len(MILESTONES))
    for i, m in enumerate(MILESTONES):
        with cols[i]:
            _pill(LABELS[m], bool(status.get(m)))

    # spacing below pills for clarity
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

def show_intake_summary(lead: dict):
    """Compact header with client context pulled from the CRM lead dict."""
    name = lead.get("name", "—")
    city  = lead.get("city", "—")
    status = (lead.get("status","") or "—")
    assigned = lead.get("assigned_to") or "Unassigned"
    budget = lead.get("budget", 0)
    timeline = lead.get("timeline","—")

    st.markdown("###")
    st.markdown(f"**{name}** — {city} &nbsp;&nbsp;•&nbsp;&nbsp; **Assigned:** {assigned}")
    cols = st.columns([1,1,1,2])
    with cols[0]:
        st.caption("Status")
        st.write(status)
    with cols[1]:
        st.caption("Budget / mo")
        st.write(f"${int(budget):,}" if budget else "—")
    with cols[2]:
        st.caption("Timeline")
        st.write(timeline)
    with cols[3]:
        st.caption("Notes")
        st.write(lead.get("notes") or "—")
