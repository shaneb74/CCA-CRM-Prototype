# pages/90_Intake_Workflow.py
# Intake Workflow — minimal update: highlight active chip + auto-open matching drawer
from __future__ import annotations
import datetime as _dt
import streamlit as st

# ---- helpers to read/write intake step state (non-destructive) ----------------
def _get_lead_id() -> str | None:
    try:
        return st.session_state.get("selected_lead_id") or st.session_state.get("selected_lead")
    except Exception:
        return None

def _ensure_steps(lead_id: str) -> dict:
    st.session_state.setdefault("case_steps", {})
    steps = st.session_state["case_steps"].setdefault(lead_id, {})
    steps.setdefault("intake", {
        "lead_received": True,            # already in system
        "lead_assigned": False,
        "initial_contact_attempted": False,
        "initial_contact_made": False,
        "consultation_scheduled": False,
        "assessment_started": False,
        "assessment_completed": False,
        "qualification_decision": False,
    })
    return steps["intake"]

def _first_incomplete_index(steps: dict, order: list[str]) -> int:
    for i, key in enumerate(order):
        if not steps.get(key, False):
            return i
    return len(order) - 1

# ---- page --------------------------------------------------------------------
st.set_page_config(page_title="Intake Workflow", page_icon="👣", layout="wide")

try:
    import store
except Exception:
    store = None

lead_id = _get_lead_id()
if not lead_id and store:
    # Fallback to previously selected lead in store
    lead_id = getattr(store, "get_selected_lead_id", lambda: None)()

if not lead_id:
    st.info("Select a client in Client Record first.")
    st.stop()

lead = None
if store:
    try:
        lead = store.get_lead(lead_id)
    except Exception:
        lead = None

if not lead:
    lead = {"id": lead_id, "name": "Unknown", "city": "", "status": "new",
            "budget": 0, "timeline": "—", "assigned_to": ""}

steps_order = [
    ("lead_received", "Lead received"),
    ("lead_assigned", "Lead assigned"),
    ("initial_contact_attempted", "Initial contact attempted"),
    ("initial_contact_made", "Initial contact made"),
    ("consultation_scheduled", "Consultation scheduled"),
    ("assessment_started", "Assessment started"),
    ("assessment_completed", "Assessment completed"),
    ("qualification_decision", "Qualification decision"),
]
step_keys = [k for k,_ in steps_order]

steps = _ensure_steps(lead_id)
active_idx = _first_incomplete_index(steps, step_keys)

# --- minimal css to ONLY add active highlighting to the existing rectangular chips
st.markdown("""
<style>
.cca-chip-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:8px}
.cca-chip{
  border:1px solid #e5e7eb;border-radius:8px;padding:8px 14px;
  background:#fafafa;color:#374151;font-size:13px;line-height:1;
}
.cca-chip.active{
  border-color:#2563eb;background:#eff6ff;color:#1d4ed8;font-weight:600;
  box-shadow:0 0 0 2px rgba(37,99,235,.08) inset;
}
/* keep drawers width reasonable on large screens */
.cca-two-col{display:grid;grid-template-columns:1.3fr .8fr;gap:24px}
@media (max-width: 1100px){
  .cca-two-col{grid-template-columns:1fr}
}
</style>
""", unsafe_allow_html=True)

# ---- header area (kept as-is; only data values filled) ------------------------
st.title("Intake Workflow")
c1, c2, c3, c4 = st.columns([2,1,1,1])
with c1:
    st.markdown(f"**{lead.get('name','')}** • {lead.get('city','')}")
    st.caption(f"Assigned: {lead.get('assigned_to') or 'Unassigned'}")
with c2:
    st.caption("Status")
    st.write(lead.get("status","new"))
with c3:
    st.caption("Budget / mo")
    budget = lead.get("budget", 0) or 0
    st.write(f\"{int(budget):,}\" if budget else "—")
with c4:
    st.caption("Timeline")
    st.write(lead.get("timeline","—"))

st.divider()

# ---- chip row (exactly one 'active') ------------------------------------------
st.caption("Intake progress")
st.markdown('<div class="cca-chip-row">' + "".join([
    f'<div class="cca-chip {"active" if i==active_idx else ""}">{label}</div>'
    for i, (key,label) in enumerate(steps_order)
]) + "</div>", unsafe_allow_html=True)

# ---- optional thin progress (kept subtle) -------------------------------------
prog = (active_idx)/max(1,(len(steps_order)-1))
st.progress(min(max(prog,0.0),1.0))

# ---- two column: drawers + case snapshot --------------------------------------
st.markdown('<div class="cca-two-col">', unsafe_allow_html=True)

# left: drawers
st.markdown("<div>", unsafe_allow_html=True)
for i, (key, label) in enumerate(steps_order):
    with st.expander(label, expanded=(i==active_idx)):
        colA, colB = st.columns([1,1])
        with colA:
            st.checkbox("Mark complete", value=bool(steps.get(key, False)),
                        key=f"chk_{key}")
        with colB:
            if key == "lead_assigned":
                st.text_input("Assigned to", value=lead.get("assigned_to") or "", key="assigned_to_tmp")
            elif key == "initial_contact_attempted":
                st.selectbox("Method", ["Phone","Email","SMS"], index=0, key="ica_method")
                st.text_input("Outcome", value="", key="ica_outcome")
            elif key == "initial_contact_made":
                st.date_input("Contact date", value=_dt.date.today(), key="icm_date")
                st.text_input("Notes", value="", key="icm_notes")
            elif key == "consultation_scheduled":
                st.date_input("Consultation date", value=_dt.date.today(), key="cs_date")
                st.time_input("Time", key="cs_time")
            elif key == "assessment_started":
                st.selectbox("Who provided info", ["Resident","Child","POA","Other"], key="as_who")
            elif key == "assessment_completed":
                st.text_area("Summary", value="", key="ac_summary")
            elif key == "qualification_decision":
                st.selectbox("Decision", ["Qualified","Deferred","Declined"], key="qd_decision")
# right: snapshot
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div>", unsafe_allow_html=True)
st.subheader("Case snapshot")
st.write(f"**{lead.get('name','')}** • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")
st.write(f"**Care preference:** {lead.get('preference','—')}")
if budget:
    st.write(f"**Budget:** ${int(budget):,}/mo")
else:
    st.write("**Budget:** —")
st.write(f"**Timeline:** {lead.get('timeline','—')}")
if lead.get("notes"):
    st.write(f"**Notes:** {lead.get('notes')}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end grid

# ---- footer buttons (unchanged) -----------------------------------------------
lc, rc = st.columns([1,1])
with lc:
    if st.button("Complete Intake → Start Placement", key="btn_complete_intake"):
        # mark all as complete and suggest next
        for k,_ in steps_order:
            steps[k] = True
        st.session_state["case_steps"][lead_id]["intake"] = steps
        # schedule navigation if switch_page is available elsewhere
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.experimental_rerun()
with rc:
    st.button("← Back to Workflows", key="btn_back_workflows")

# ---- persist checkboxes back to steps -----------------------------------------
changed = False
for key,_ in steps_order:
    ui_key = f"chk_{key}"
    if ui_key in st.session_state:
        val = bool(st.session_state[ui_key])
        if steps.get(key) != val:
            steps[key] = val
            changed = True

if changed:
    st.session_state["case_steps"][lead_id]["intake"] = steps
    # recompute active and reopen that drawer on the next render
    st.experimental_rerun()
