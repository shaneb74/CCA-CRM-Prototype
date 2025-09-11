# pages/90_Intake_Workflow.py
# Intake Workflow — keep original layout; add active-chip highlight + auto-open drawer

from __future__ import annotations
import datetime as dt
import streamlit as st

import store  # uses: init(), get_selected_lead_id(), get_lead(), set_selected_lead(), get_progress()

# --- safe page config (avoid multiple set_page_config crashes) ---
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
    """
    We keep per-lead intake steps in st.session_state.case_steps[lead_id] as a list of bools,
    one per STAGES entry. If missing, initialize with first step done (received).
    """
    st.session_state.setdefault("case_steps", {})
    steps = st.session_state["case_steps"].get(lead_id)
    if not steps or len(steps) != len(STAGES):
        steps = [False] * len(STAGES)
        # If lead exists in system, mark "Lead received" True by default.
        steps[0] = True
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
    return max(0.0, min(1.0, done / float(len(steps))))

def _sla_for_stage(idx: int, received_at: dt.datetime | None) -> tuple[str, str, str]:
    """
    Very light SLA text for banner: (next_label, status_emoji, due_str)
    Uses the spec you provided; times are illustrative.
    """
    # map simple SLAs (hours/days) to each stage
    SLA_RULES = {
        1: dt.timedelta(hours=8),     # Lead assigned within same business day
        2: dt.timedelta(hours=2),     # Initial attempt within 2 business hours
        3: dt.timedelta(days=2),      # Initial contact made -> schedule within 2 days
        4: dt.timedelta(days=2),      # Consultation scheduled within 2 days of contact
        5: dt.timedelta(days=3),      # Assessment started within 3 business days
        6: dt.timedelta(days=5),      # Assessment completed within 5 business days of consult
        7: dt.timedelta(hours=0),     # Decision — no SLA here in prototype
    }
    next_idx = min(idx, len(STAGES)-1)
    label = STAGES[next_idx]
    base = received_at or dt.datetime.utcnow()
    due = base + SLA_RULES.get(next_idx, dt.timedelta(days=2))
    # Simple on-track indicator (real impl would compare now to due & stage start time)
    status = "✅ On track"
    return label, status, due.strftime("%Y-%m-%d %H:%M UTC")

def _chip(label: str, state: str):
    """
    Render a rectangular chip with state:
      state in {"active", "done", "future"}
    """
    CSS = """
    <style>
    .chip-row{display:flex;gap:.75rem;flex-wrap:wrap}
    .chip{padding:.35rem .7rem;border-radius:.5rem;border:1px solid var(--border,#e5e7eb);
          background: var(--bg,#fff); color: var(--fg,#6b7280); font-size:.85rem;}
    .chip.done{--bg:#f9fafb; --border:#d1d5db; --fg:#6b7280}
    .chip.active{--bg:#e8f1ff; --border:#2563eb; --fg:#1f2937; box-shadow:0 0 0 2px rgba(37,99,235,.15) inset}
    </style>
    """
    classes = "chip " + state
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(f'<div class="{classes}">{label}</div>', unsafe_allow_html=True)

def _two_col() -> tuple:
    # Keep your original proportions so Case snapshot sits to the right
    return st.columns([3, 2], gap="large")

def _pill(label: str, value: str):
    st.markdown(
        f"""
        <div style="
            display:inline-block;padding:.55rem .9rem;border-radius:.5rem;
            background:#f3f4f6;color:#111827;font-size:.875rem;border:1px solid #e5e7eb;">
            <strong style="color:#6b7280">{label}:</strong> {value}
        </div>
        """,
        unsafe_allow_html=True,
    )

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

# Header row (kept)
top = st.columns([2,1,1,1,1])
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
with top[4]:
    st.caption("")  # spacer

# Origin / Received pills (kept)
pcols = st.columns([1,1,6])
with pcols[0]:
    _pill("Origin", origin)
with pcols[1]:
    _pill("Received", "just now")

# Compute stage state
steps = _steps_state_for_lead(lead_id)
active_idx = _active_index(steps)

# Horizontal chips row (kept; add highlight)
st.write("")  # tiny spacer
st.markdown('<div class="chip-row">', unsafe_allow_html=True)
for i, label in enumerate(STAGES):
    state = "active" if i == active_idx else ("done" if steps[i] and i < active_idx else "done" if steps[i] else "future")
    _chip(label, state)
st.markdown('</div>', unsafe_allow_html=True)

# SLA banner + progress (kept)
next_label, next_status, due_str = _sla_for_stage(max(active_idx, 1), dt.datetime.utcnow())
st.markdown(f"**Next action:** {next_label} · {next_status} · **Due:** {due_str}")
st.progress(_progress_percent(steps))

# ---------- Body: left drawers + right Case snapshot (kept) ----------

left, right = _two_col()

with left:
    # Build each expander; auto-open the active one
    for i, label in enumerate(STAGES):
        with st.expander(label, expanded=(i == active_idx)):
            if i == 1:
                # Example minimal content for "Lead assigned"
                c1, c2 = st.columns([1,2])
                with c1:
                    st.checkbox("Mark complete", key=f"step_{i}_done", value=steps[i])
                with c2:
                    st.caption("Assigned to")
                    st.write(assigned)
            else:
                st.caption("")

with right:
    st.subheader("Case snapshot")
    st.write(f"**{name}** • {city} • **Assigned:** {assigned}")
    pref = lead.get("preference") or lead.get("ds_recommendation") or "—"
    st.write(f"**Care preference:** {pref}")
    st.write(f"**Budget:** {'$'+format(int(budget),',')+'/mo' if budget else '—'}")
    st.write(f"**Timeline:** {timeline}")
    notes = lead.get("notes") or "—"
    st.write(f"**Notes:** {notes}")

# ---------- Footer actions (kept) ----------

f1, f2 = st.columns([1,1])
with f1:
    if st.button("Complete Intake → Start Placement", type="primary"):
        # Mark all steps complete for demo
        steps[:] = [True] * len(STAGES)
        st.session_state["case_steps"][lead_id] = steps
        # schedule redirect (no rerun here)
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
with f2:
    if st.button("← Back to Workflows"):
        st.session_state["_goto_page"] = "pages/89_Workflows.py"
