
import streamlit as st
from datetime import date

PILL_GAP_X = 10
PILL_GAP_Y = 10

def _pill_style():
    return f"""
    <style>
      .cca-pill-row {{
         display:flex; flex-wrap:wrap; gap:{PILL_GAP_X}px {PILL_GAP_Y}px; margin: 6px 0 14px 0;
      }}
      .cca-pill {{
         display:inline-flex; align-items:center; gap:6px;
         padding: 4px 10px; border-radius: 999px; font-size:12px; line-height:1;
         border:1px solid #e5e7eb; background:#f9fafb; color:#374151;
      }}
      .cca-pill.done {{ background:#ecfdf5; border-color:#a7f3d0; color:#065f46; }}
      .cca-pill.overdue {{ background:#fff7ed; border-color:#fed7aa; color:#9a3412; }}
      .cca-pill.duetoday {{ background:#fffbeb; border-color:#fde68a; color:#92400e; }}
    </style>
    """

def _state_class(step):
    if step.get("completed"):
        return "done"
    due = step.get("sla_due")
    if isinstance(due, date):
        today = date.today()
        if due < today:
            return "overdue"
        if due == today:
            return "duetoday"
    return ""

def render_pills(steps: list[dict]):
    st.markdown(_pill_style(), unsafe_allow_html=True)
    html = ['<div class="cca-pill-row">']
    for s in steps:
        cls = _state_class(s)
        label = s.get("label", "Step")
        html.append(f'<div class="cca-pill {cls}">{label}</div>')
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)

def progress_fraction(steps: list[dict]) -> float:
    if not steps: 
        return 0.0
    done = sum(1 for s in steps if s.get("completed"))
    return round(done / len(steps), 4)

def first_incomplete_index(steps: list[dict]) -> int:
    for idx, s in enumerate(steps):
        if not s.get("completed"):
            return idx
    return 0
