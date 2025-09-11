# pages/90_Intake_Workflow.py
# Intake Workflow — keep original layout; add active-chip highlight + auto-open drawer

from __future__ import annotations
import datetime as dt
import streamlit as st

import store  # uses: init(), get_selected_lead_id(), get_lead()

# --- safe page config ---
try:
    st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
except Exception:
    pass

store.init()

# ---------- helpers ----------

STAGES: list[str] = [
    "Lead received",
    "Lead assigned",
    "Initial contact attempted",
    "Initial contact made",
    "Consultation scheduled",
    "Assessment started",
    "Assessment completed",
    "Qualification decision",
]

def _steps_state_for_lead(lead_id: str) -> list[bool]:
    """Per-lead intake steps stored in session_state."""
    st.session_state.setdefault("case_steps", {})
    steps = st.session_state["case_steps"].get(lead_id)
    if not steps or len(steps) != len(STAGES):
        steps = [False] * len(STAGES)
        steps[0] = True  # default: received
        st.session_state["case_steps"][lead_id] = steps
    return steps

def _active_index(steps: list[bool]) -> int:
    """First incomplete index; if all complete, return last index."""
    for i, done in enumerate(steps):
        if not done:
            return i
    return len(steps) - 1

def _progress_percent(steps: list[bool]) -> float:
    done = sum(1 for x in steps if x)
    return max(0.0, min(1.0, done / float(len(STAGES))))

def _sla_for_stage(idx: int, received_at: dt.datetime | None) -> tuple[str, str, str]:
    SLA_RULES = {
        1: dt.timedelta(hours=8),
        2: dt.timedelta(hours=2),
        3: dt.timedelta(days=2),
        4: dt.timedelta(days=2),
        5: dt.timedelta(days=3),
        6: dt.timedelta(days=5),
        7: dt.timedelta(hours=0),
    }
    next_idx = min(idx, len(STAGES)-1)
    label = STAGES[next_idx]
    base = received_at or dt.datetime.utcnow()
    due = base + SLA_RULES.get(next_idx, dt.timedelta(days=2))
    status = "✅ On track"
    return label, status, due.strftime("%Y-%m-%d %H:%M UTC")

def _pill(label: str, value: str):
    st.markdown(
        f"""
        <div style="
            display:inline-block;padding:.55rem .9rem;border-radius:.5rem;
            background:#f3f4f6;color:#111827;font-size:.875rem;border:1px solid #e5e7eb;
            margin-right:.5rem;">
            <strong style="color:#6b7280">{label}:</strong> {value}
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- CSS for chips ---
st.markdown("""
<style>
.chip-row{display:flex;gap:.75rem;flex-wrap:wrap;margin:.5rem 0}
.chip{padding:.35rem .7rem;border-radius:.5rem;border:1px solid #e5e7eb;
      background:#fafafa;color:#6b7280;font-size:.85rem;}
.chip.done{background:#f9fafb;border-color:#d1d5db;color:#6b7280}
.chip.active{background:#e8f1ff;border-color:#2563eb;color:#1f2937;
             font-weight:600;box-shadow:0 0 0 2px rgba(37,99,235,.15) inset}
</style>
""", unsafe_allow_html=True)

# ---------- page data ----------

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")

if not lead:
    st.info("Select a client in **Client Record** or the **Workflows** hub first.")
    st.stop()

name = lead.get("name","")
city = lead.get("city","")
status = str(lead.get("status","")).replace("_"," ")
budget = lead.get("budget", 0)
timeline = lead.get("timeline", "—")
assigned = lead.get("assigned_to") or "Unassigned"
origin = str(lead.get("origin","")).lower() or "app"

# Header row
top = st.columns([2,1,1,1])
with top[0]:
    st.subheader(f"{name} • {city}")
    st.caption(f"Assigned: {assigned}")
with top[1]:
    st.caption("Status")
    st.write(status)
with top[2]:
    st.caption("Budget / mo")
    st.write(f"${int(budget):,}" if budget else "—")
with top[3]:
    st.caption("Timeline")
    st.write(timeline)

# Origin / Received pills
pcols = st.columns([1,1,5])
with pcols[0]:
    _pill("Origin", origin)
with pcols[1]:
    _pill("Received", "just now")

# Compute stage state
steps = _steps_state_for_lead(lead_id)
active_idx = _active_index(steps)

# Horizontal chips row
chip_html = ['<div class="chip-row">']
for i, label in enumerate(STAGES):
    state = "active" if i == active_idx else ("done" if steps[i] and i < active_idx else "future")
    chip_html.append(f'<div class="chip {state}">{label}</div>')
chip_html.append('</div>')
st.markdown("".join(chip_html), unsafe_allow_html=True)

# SLA banner + progress
next_label, next_status, due_str = _sla_for_stage(max(active_idx, 1), dt.datetime.utcnow())
st.markdown(f"**Next action:** {next_label} · {next_status} · **Due:** {due_str}")
st.progress(_progress_percent(steps))

# ---------- Body: left drawers + right Case snapshot ----------

left, right = st.columns([3,2], gap="large")

with left:
    for i, label in enumerate(STAGES):
        with st.expander(label, expanded=(i == active_idx)):
            st.checkbox("Mark complete", key=f"step_{i}", value=steps[i])

with right:
    st.subheader("Case snapshot")
    st.write(f"**{name}** • {city} • **Assigned:** {assigned}")
    pref = lead.get("preference") or lead.get("ds_recommendation") or "—"
    st.write(f"**Care preference:** {pref}")
    st.write(f"**Budget:** {'$'+format(int(budget),',')+'/mo' if budget else '—'}")
    st.write(f"**Timeline:** {timeline}")
    notes = lead.get("notes") or "—"
    st.write(f"**Notes:** {notes}")

# ---------- Footer actions ----------

f1, f2 = st.columns([1,1])
with f1:
    if st.button("Complete Intake → Start Placement", type="primary"):
        steps[:] = [True] * len(STAGES)
        st.session_state["case_steps"][lead_id] = steps
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
with f2:
    if st.button("← Back to Workflows"):
        st.session_state["_goto_page"] = "pages/89_Workflows.py"
