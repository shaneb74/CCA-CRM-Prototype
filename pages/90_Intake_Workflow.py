# pages/90_Intake_Workflow.py
from __future__ import annotations
import datetime as dt
import streamlit as st

# --- Optional UI helpers (safe if missing) ---
try:
    from ui_chrome import apply_chrome  # handles page config + any redirect
    apply_chrome()
except Exception:
    pass

import store  # your data layer

# --------- constants / helpers ---------
STAGES = [
    "Lead received",
    "Lead assigned",
    "Initial contact attempted",
    "Initial contact made",
    "Consultation scheduled",
    "Assessment started",
    "Assessment completed",
    "Qualification decision",
]

def _get_steps(lead: dict) -> list[bool]:
    # Persisted boolean list in the lead record; create if absent
    steps = lead.get("intake_steps")
    if not isinstance(steps, list) or len(steps) != len(STAGES):
        steps = [False] * len(STAGES)
    return steps

def _set_steps(lead: dict, steps: list[bool]) -> None:
    lead["intake_steps"] = steps
    store.upsert_lead(lead)

def _active_index(steps: list[bool]) -> int:
    # first incomplete step; if all complete, last index
    for i, done in enumerate(steps):
        if not done:
            return i
    return len(steps) - 1

def _progress_pct(steps: list[bool]) -> float:
    return sum(1 for s in steps if s) / len(steps) if steps else 0.0

def _sla_due_for(index: int, received_ts: dt.datetime) -> dt.datetime:
    """
    Toy SLA model for the prototype:
      0 Lead received               -> now
      1 Lead assigned               -> +2 hours
      2 Initial contact attempted   -> +2 hours
      3 Initial contact made        -> +2 days
      4 Consultation scheduled      -> +2 days
      5 Assessment started          -> +3 business days (approx 3 days)
      6 Assessment completed        -> +5 business days (approx 5 days)
      7 Qualification decision      -> +1 day
    """
    offsets = [
        dt.timedelta(hours=0),
        dt.timedelta(hours=2),
        dt.timedelta(hours=2),
        dt.timedelta(days=2),
        dt.timedelta(days=2),
        dt.timedelta(days=3),
        dt.timedelta(days=5),
        dt.timedelta(days=1),
    ]
    base = received_ts or dt.datetime.utcnow()
    return base + offsets[min(index, len(offsets) - 1)]

def _badge(text: str) -> str:
    return f"""
    <span style="
        display:inline-block;border-radius:.5rem;
        background:#eef2ff;color:#374151;
        padding:.5rem .75rem;border:1px solid #e5e7eb;
        font-size:.85rem;">{text}</span>
    """

# ---------- page ----------
store.init()
lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")

if not lead:
    st.info("Select a client in **Client Record** first.")
    st.stop()

# make lead accessible from other pages that might set redirects
st.session_state["_lead_obj"] = lead

name = lead.get("name", "—")
city = lead.get("city", "—")
assigned_to = lead.get("assigned_to") or "Unassigned"
status = lead.get("status", "new")
budget = lead.get("budget", 0)
timeline = lead.get("timeline", "—")
origin = (lead.get("origin") or "app").lower()
received_iso = lead.get("received_at") or dt.datetime.utcnow().isoformat()
try:
    received_dt = dt.datetime.fromisoformat(received_iso.replace("Z", "+00:00"))
except Exception:
    received_dt = dt.datetime.utcnow()

steps = _get_steps(lead)
active_idx = _active_index(steps)
pct = _progress_pct(steps)

# --- page header line (kept minimal like your working design) ---
hdr_cols = st.columns([3, 2, 2, 2])
with hdr_cols[0]:
    st.subheader(f"{name} • {city}")
    st.caption(f"Assigned: {assigned_to}")
with hdr_cols[1]:
    st.caption("Status")
    st.write(status)
with hdr_cols[2]:
    st.caption("Budget / mo")
    st.write(f"{int(budget):,}" if budget else "—")
with hdr_cols[3]:
    st.caption("Timeline")
    st.write(timeline)

# --- origin / received badges row ---
st.markdown(
    f"{_badge(f'Origin: {origin}')} &nbsp; {_badge('Received: ' + _humanize_delta(received_dt))}",
    unsafe_allow_html=True,
)

# ---------- chip row (HORIZONTAL, evenly spaced, with breathing room) ----------
# CSS once for chips + page breathing
st.markdown("""
<style>
.chip-row{
  display:flex; justify-content:space-between; flex-wrap:nowrap;
  margin: 1rem 0 1.25rem 0; gap: .25rem;
}
.chip{
  flex:1; text-align:center;
  padding:.60rem 1rem;
  border:1px solid #e5e7eb; border-radius:.5rem;
  background:#fafafa; color:#6b7280; font-size:.90rem;
}
.chip.active{
  background:#e8f1ff; border-color:#2563eb; color:#1f2937; font-weight:600;
  box-shadow:0 0 0 2px rgba(37,99,235,.15) inset;
}
.progress-rail{ height:6px;background:#eef2f7;border-radius:9999px; }
.progress-fill{ height:6px;background:#3b82f6;border-radius:9999px; }
.section-spacer{ height:.75rem; }
</style>
""", unsafe_allow_html=True)

def _humanize_delta(ts: dt.datetime) -> str:
    delta = dt.datetime.utcnow().astimezone(dt.timezone.utc) - ts.astimezone(dt.timezone.utc)
    secs = int(delta.total_seconds())
    if secs < 60: return f"{secs}s ago"
    mins = secs // 60
    if mins < 60: return f"{mins}m ago"
    hrs = mins // 60
    if hrs < 24: return f"{hrs}h ago"
    days = hrs // 24
    return f"{days}d ago"

# chips
chip_html = ['<div class="chip-row">']
for i, label in enumerate(STAGES):
    cls = "chip active" if i == active_idx else "chip"
    chip_html.append(f'<div class="{cls}">{label}</div>')
chip_html.append("</div>")
st.markdown("".join(chip_html), unsafe_allow_html=True)

# SLA / next action line
due = _sla_due_for(active_idx, received_dt)
on_track = "✅ On track"  # simple prototype decoration
st.markdown(
    f"**Next action:** {STAGES[active_idx]} · {on_track} · **Due:** {due.strftime('%Y-%m-%d %H:%M UTC')}"
)

# visual progress bar
rail = st.container()
with rail:
    rail_cols = st.columns([1])
    with rail_cols[0]:
        st.markdown('<div class="progress-rail">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="progress-fill" style="width:{int(pct*100)}%"></div>',
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

# ---------- Layout: drawers left, snapshot right ----------
left, right = st.columns([7, 5], vertical_alignment="top")

with left:
    # Drawers (expanders). Auto-open the one matching active stage.
    for i, label in enumerate(STAGES):
        with st.expander(label, expanded=(i == active_idx)):
            # For demo, keep content minimal but include one actionable control
            if i == 1:  # Lead assigned
                colA, colB = st.columns([1, 2])
                with colA:
                    done = st.checkbox("Mark complete", key=f"done_{i}", value=steps[i])
                with colB:
                    st.caption(f"Assigned to")
                    st.write(assigned_to)
                if done != steps[i]:
                    steps[i] = done
                    _set_steps(lead, steps)
                    st.rerun()
            else:
                # Generic toggler for other steps
                done = st.checkbox("Mark complete", key=f"done_{i}", value=steps[i])
                if done != steps[i]:
                    steps[i] = done
                    _set_steps(lead, steps)
                    st.rerun()

with right:
    st.subheader("Case snapshot")
    st.caption(f"{name} • {city} • Assigned: {assigned_to}")
    st.write(f"**Care preference:** {lead.get('preference', '—')}")
    st.write(f"**Budget:** {f'${int(budget):,}/mo' if budget else '—'}")
    st.write(f"**Timeline:** {timeline}")
    notes = lead.get("notes")
    if notes:
        st.write(f"**Notes:** {notes}")

# ---- Actions row ----
go_cols = st.columns([1, 4])
with go_cols[0]:
    if st.button("Complete Intake → Start Placement", type="primary"):
        # mark all steps complete and hop to placement
        steps = [True] * len(STAGES)
        _set_steps(lead, steps)
        # Store a flag and perform the redirect on top-of-run (handled by ui_chrome.apply_chrome if present)
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.rerun()

with go_cols[1]:
    st.button("← Back to Workflows", key="back_to_workflows", on_click=lambda: _schedule_nav("pages/89_Workflows.py"))

# --------- tiny util for back button without no-op warning ---------
def _schedule_nav(path: str):
    st.session_state["_goto_page"] = path
