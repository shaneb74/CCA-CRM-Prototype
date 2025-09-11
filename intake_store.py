
import streamlit as st
from datetime import datetime, timedelta

# ---- Step ordering & SLA targets (hours) ----
STEP_ORDER = [
    "lead_received",
    "lead_assigned",
    "initial_contact_attempted",
    "initial_contact_made",
    "consultation_scheduled",
    "assessment_started",
    "assessment_completed",
    "qualification_decision",
]

STEP_LABELS = {
    "lead_received": "Lead received",
    "lead_assigned": "Lead assigned",
    "initial_contact_attempted": "Initial contact attempted",
    "initial_contact_made": "Initial contact made",
    "consultation_scheduled": "Consultation scheduled",
    "assessment_started": "Assessment started",
    "assessment_completed": "Assessment completed",
    "qualification_decision": "Qualification decision",
}

SLA_HOURS = {
    "lead_received": 0,             # already done if in system
    "lead_assigned": 8,             # within same business day
    "initial_contact_attempted": 2, # within 2 business hours
    "initial_contact_made": 24*1,   # connect within 1 day
    "consultation_scheduled": 48,   # within 2 days of contact
    "assessment_started": 72,       # within 3 business days
    "assessment_completed": 120,    # within 5 business days
    "qualification_decision": 24,   # within 1 day of assessment
}

def _key(lead_id:str)->str:
    return f"intake::{lead_id}"

def _meta_key(lead_id:str)->str:
    return f"lead_meta::{lead_id}"

def init_for_lead(lead:dict):
    """
    Ensure we have intake state & meta for a lead.
    Meta keeps origin & received_at. State tracks per-step completion + ts.
    """
    lead_id = lead.get("id") or lead.get("lead_id")
    if not lead_id:
        return

    # Initialize meta (origin, received_at) once
    mk = _meta_key(lead_id)
    if mk not in st.session_state:
        st.session_state[mk] = {
            "origin": str(lead.get("origin","Unknown")),
            "received_at": datetime.utcnow().isoformat()
        }

    # Initialize state once
    k = _key(lead_id)
    if k not in st.session_state:
        # default: lead_received is complete at init with now()
        now = datetime.utcnow().isoformat()
        st.session_state[k] = {
            step: {"done": (step == "lead_received"), "ts": (now if step=="lead_received" else None)}
            for step in STEP_ORDER
        }

def get_meta(lead_id:str):
    return st.session_state.get(_meta_key(lead_id), {})

def update_meta(lead_id:str, **kwargs):
    mk = _meta_key(lead_id)
    st.session_state.setdefault(mk, {})
    st.session_state[mk].update(kwargs)

def get_state(lead_id:str):
    return st.session_state.get(_key(lead_id), {})

def mark_step(lead_id:str, step:str, done:bool=True, ts:datetime|None=None):
    k = _key(lead_id)
    st.session_state.setdefault(k, {})
    step_state = st.session_state[k].setdefault(step, {"done": False, "ts": None})
    step_state["done"] = bool(done)
    if ts is None:
        ts = datetime.utcnow()
    if done:
        step_state["ts"] = ts.isoformat()

def percent_complete(lead_id:str)->float:
    s = get_state(lead_id)
    if not s:
        return 0.0
    total = len(STEP_ORDER)
    done = sum(1 for step in STEP_ORDER if s.get(step,{}).get("done"))
    return done/total if total else 0.0

def next_step(lead_id:str):
    s = get_state(lead_id)
    for step in STEP_ORDER:
        if not s.get(step,{}).get("done"):
            return step
    return None

def _step_completed_at(lead_id:str, step:str):
    s = get_state(lead_id)
    ts = s.get(step,{}).get("ts")
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return None

def _step_index(step:str)->int:
    try:
        return STEP_ORDER.index(step)
    except ValueError:
        return -1

def sla_status(lead_id:str):
    """
    Returns (step_key, due_dt_utc, status_str) for the NEXT step.
    status_str: 'ok' | 'due_soon' | 'overdue'
    Heuristic: 'due_soon' if within 25% of deadline remaining (<25% buffer).
    """
    nxt = next_step(lead_id)
    if not nxt:
        return (None, None, "ok")
    idx = _step_index(nxt)
    # base time is completion of previous step (or received_at for first)
    if idx <= 0:
        base_ts = get_meta(lead_id).get("received_at")
        base_dt = datetime.fromisoformat(base_ts) if base_ts else datetime.utcnow()
    else:
        prev = STEP_ORDER[idx-1]
        base_dt = _step_completed_at(lead_id, prev) or datetime.utcnow()

    hours = SLA_HOURS.get(nxt, 0)
    due = base_dt + timedelta(hours=hours)

    now = datetime.utcnow()
    if now > due:
        status = "overdue"
    else:
        total = (due - base_dt).total_seconds()
        left = (due - now).total_seconds()
        status = "due_soon" if total and (left/total) < 0.25 else "ok"
    return (nxt, due, status)

def human_when(dt:datetime|None)->str:
    if not dt: return "—"
    delta = datetime.utcnow() - dt
    s = int(delta.total_seconds())
    if s < 60: return f"{s}s ago"
    m = s//60
    if m < 60: return f"{m}m ago"
    h = m//60
    if h < 24: return f"{h}h ago"
    d = h//24
    return f"{d}d ago"
