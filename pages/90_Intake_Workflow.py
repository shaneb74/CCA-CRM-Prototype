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
        <div class="pill">
            <strong style="color:#6b7280">{label}:</strong> {value}
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- CSS for improved visual layout ---
st.markdown("""
<style>
/* General page styling */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #111827;
}

/* Header section */
.header-container {
    background: #f9fafb;
    padding: 1rem;
    border-bottom: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}
.header-subheader {
    font-size: 1.5rem;
    font-weight: 600;
    color: #111827;
}
.header-caption {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 0.25rem;
}
.header-column {
    border-right: 1px solid #e5e7eb;
    padding: 0.75rem;
}
.header-column:last-child {
    border-right: none;
}
.status-critical {
    font-weight: 600;
    color: #1f2937;
}

/* Pills */
.pill-container {
    background: #f9fafb;
    padding: 0.75rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}
.pill {
    display: inline-block;
    padding: 0.65rem 1rem;
    border-radius: 0.5rem;
    background: #e5e7eb;
    color: #111827;
    font-size: 0.875rem;
    border: 1px solid #d1d5db;
    margin-right: 0.5rem;
    transition: background 0.2s;
}
.pill:hover {
    background: #d1d5db;
}

/* Chips */
.chip-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    max-width: 100%;
    padding: 0.75rem 0;
}
.chip {
    padding: 0.35rem 0.7rem;
    border-radius: 0.5rem;
    border: 1px solid #e5e7eb;
    background: #ffffff;
    color: #9ca3af;
    font-size: 0.85rem;
}
.chip.done {
    background: #f3f4f6;
    border-color: #9ca3af;
    color: #6b7280;
}
.chip.active {
    background: #e8f1ff;
    border-color: #2563eb;
    color: #1f2937;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: 0 0 0 3px rgba(37,99,235,.25) inset;
}

/* SLA and Progress */
.sla-progress-container {
    border: 1px solid #e5e7eb;
    background: #f9fafb;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
.sla-text {
    font-weight: 600;
    color: #111827;
}
.sla-status-ontrack {
    color: #15803d;
}
.progress-label {
    font-size: 0.85rem;
    color: #6b7280;
    text-align: center;
    margin-top: 0.25rem;
}
.stProgress > div > div > div > div {
    background: linear-gradient(to right, #2563eb, #3b82f6);
}

/* Expanders and Case Snapshot */
.expander {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    padding: 1rem;
}
.expander-active {
    background: #e8f1ff;
}
.checkbox-label:hover {
    background: #f3f4f6;
    border-radius: 0.25rem;
}
.case-snapshot {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,.1);
}
.snapshot-field {
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
}
.snapshot-label {
    font-weight: 600;
    color: #111827;
}

/* Footer */
.footer-container {
    border-top: 1px solid #e5e7eb;
    padding-top: 1rem;
    display: flex;
    gap: 1rem;
    justify-content: center;
}
.primary-button {
    background: #2563eb !important;
    color: #ffffff !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 0.5rem !important;
}
.secondary-button {
    background: #ffffff !important;
    border: 1px solid #2563eb !important;
    color: #2563eb !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 0.5rem !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .header-column, .main-columns {
        flex-direction: column;
        gap: 1rem;
    }
    .chip-row {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- page data ----------
lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None
st.title("Intake Workflow")
if not lead:
    st.info("Select a client in **Client Record** or the **Workflows** hub first.")
    st.stop()

name = lead.get("name", "")
city = lead.get("city", "")
status = str(lead.get("status", "")).replace("_", " ")
budget = lead.get("budget", 0)
timeline = lead.get("timeline", "—")
assigned = lead.get("assigned_to") or "Unassigned"
origin = str(lead.get("origin", "")).lower() or "app"

# Header row
with st.container():
    with st.markdown('<div class="header-container">', unsafe_allow_html=True):
        top = st.columns([2, 1, 1, 1])
        with top[0]:
            st.markdown(f'<div class="header-subheader">{name} • {city}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="header-caption">Assigned: {assigned}</div>', unsafe_allow_html=True)
        with top[1]:
            st.markdown('<div class="header-caption">Status</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="status-critical">{status}</div>', unsafe_allow_html=True)
        with top[2]:
            st.markdown('<div class="header-caption">Budget / mo</div>', unsafe_allow_html=True)
            st.write(f"${int(budget):,}" if budget else "—")
        with top[3]:
            st.markdown('<div class="header-caption">Timeline</div>', unsafe_allow_html=True)
            st.write(timeline)

# Origin / Received pills
with st.container():
    with st.markdown('<div class="pill-container">', unsafe_allow_html=True):
        cols = st.columns([1, 1])
        with cols[0]:
            _pill("Origin", origin)
        with cols[1]:
            _pill("Received", "just now")

# Compute stage state
steps = _steps_state_for_lead(lead_id)
active_idx = _active_index(steps)

# Horizontal chips row
chip_html = ['<div class="chip-row">']
for i, label in enumerate(STAGES):
    state = "active" if i == active_idx else ("done" if steps[i] and i < active_idx else "")
    chip_html.append(f'<div class="chip {state}">{label}</div>')
chip_html.append('</div>')
st.markdown("".join(chip_html), unsafe_allow_html=True)

# SLA banner + progress
with st.container():
    with st.markdown('<div class="sla-progress-container">', unsafe_allow_html=True):
        next_label, next_status, due_str = _sla_for_stage(max(active_idx, 1), dt.datetime.utcnow())
        st.markdown(
            f'<div class="sla-text">Next action: {next_label} · '
            f'<span class="sla-status-ontrack">{next_status}</span> · '
            f'Due: {due_str}</div>',
            unsafe_allow_html=True
        )
        progress = _progress_percent(steps)
        st.progress(progress)
        st.markdown(f'<div class="progress-label">{int(progress*100)}% Complete</div>', unsafe_allow_html=True)

# Body: left drawers + right Case snapshot
with st.container():
    left, right = st.columns([2.5, 2], gap="large")
    with left:
        for i, label in enumerate(STAGES):
            with st.expander(label, expanded=(i == active_idx)):
                st.markdown(f'<div class="expander{" expander-active" if i == active_idx else ""}">', unsafe_allow_html=True)
                st.checkbox("Mark complete", key=f"step_{i}", value=steps[i])
                st.markdown('</div>', unsafe_allow_html=True)
    with right:
        with st.markdown('<div class="case-snapshot">', unsafe_allow_html=True):
            st.subheader("Case snapshot")
            st.markdown(f'<div class="snapshot-field"><span class="snapshot-label">Client:</span> {name} • {city}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="snapshot-field"><span class="snapshot-label">Assigned:</span> {assigned}</div>', unsafe_allow_html=True)
            pref = lead.get("preference") or lead.get("ds_recommendation") or "—"
            st.markdown(f'<div class="snapshot-field"><span class="snapshot-label">Care preference:</span> {pref}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="snapshot-field"><span class="snapshot-label">Budget:</span> {"$"+format(int(budget),",")+"/mo" if budget else "—"}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="snapshot-field"><span class="snapshot-label">Timeline:</span> {timeline}</div>', unsafe_allow_html=True)
            notes = lead.get("notes") or "—"
            st.markdown(f'<div class="snapshot-field"><span class="snapshot-label">Notes:</span> {notes}</div>', unsafe_allow_html=True)

# Footer actions
with st.container():
    with st.markdown('<div class="footer-container">', unsafe_allow_html=True):
        f1, f2 = st.columns([1, 1])
        with f1:
            if st.button("Complete Intake → Start Placement", type="primary"):
                steps[:] = [True] * len(STAGES)
                st.session_state["case_steps"][lead_id] = steps
                st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        with f2:
            if st.button("← Back to Workflows", type="secondary"):
                st.session_state["_goto_page"] = "pages/89_Workflows.py"
