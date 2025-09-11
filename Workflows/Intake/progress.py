# Workflows/Intake/progress.py
from __future__ import annotations
import streamlit as st

# Ordered milestones
MILESTONES = [
    ("lead_received",          "Lead received"),
    ("lead_assigned",          "Lead assigned"),
    ("initial_contact_attempt","Initial contact attempted"),
    ("initial_contact_made",   "Initial contact made"),
    ("consultation_scheduled", "Consultation scheduled"),
    ("assessment_started",     "Assessment started"),
    ("assessment_completed",   "Assessment completed"),
    ("qualified",              "Qualified / decision"),
]

def _key(lead_id: str) -> str:
    return f"_intake_status::{lead_id}"

def _ensure_state(lead_id: str):
    key = _key(lead_id)
    if key not in st.session_state:
        st.session_state[key] = {k: False for k,_ in MILESTONES}
        st.session_state[key]["lead_received"] = True

def set_step(lead_id: str, step_key: str, value: bool=True):
    _ensure_state(lead_id)
    st.session_state[_key(lead_id)][step_key] = bool(value)

def get_status(lead_id: str) -> dict:
    _ensure_state(lead_id)
    return dict(st.session_state[_key(lead_id)])

def progress_fraction(lead_id: str) -> float:
    s = get_status(lead_id)
    total = len(MILESTONES)
    done = sum(1 for k,_ in MILESTONES if s.get(k))
    return max(0.0, min(1.0, done/total))

def _render_stepper(status: dict):
    css = """
    <style>
      .stepper{display:flex;gap:.5rem;flex-wrap:wrap;margin:.5rem 0 0;}
      .pill{font-size:12px;border-radius:999px;padding:.25rem .6rem;border:1px solid #e5e7eb;color:#6b7280;background:#f9fafb}
      .pill.done{background:#10b98110;border-color:#34d399;color:#065f46}
      .pill .dot{display:inline-block;width:.5rem;height:.5rem;border-radius:50%;background:#d1d5db;margin-right:.35rem;vertical-align:middle}
      .pill.done .dot{background:#10b981}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    html = ['<div class="stepper">']
    for k,label in MILESTONES:
        done = "done" if status.get(k) else ""
        html.append(f'<span class="pill {done}"><span class="dot"></span>{label}</span>')
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)

def show_intake_progress(lead: dict, title: str="Intake progress"):
    if not lead:
        return
    lead_id = lead.get("id") or "UNKNOWN"
    _ensure_state(lead_id)
    s = get_status(lead_id)
    pct = progress_fraction(lead_id)

    st.subheader(title)
    st.progress(pct)

    _render_stepper(s)

    with st.expander("Update milestones (demo controls)"):
        cols = st.columns(2)
        left = [m for i,m in enumerate(MILESTONES) if i%2==0]
        right = [m for i,m in enumerate(MILESTONES) if i%2==1]
        for k,label in left:
            v = st.checkbox(label, value=s.get(k,False), key=f"ck_{lead_id}_{k}")
            if v != s.get(k):
                set_step(lead_id, k, v)
        with cols[1]:
            for k,label in right:
                v = st.checkbox(label, value=s.get(k,False), key=f"ck_{lead_id}_{k}")
                if v != s.get(k):
                    set_step(lead_id, k, v)