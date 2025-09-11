# pages/90_Intake_Workflow.py
from __future__ import annotations
import datetime as _dt
import streamlit as st
try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    try:
        st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
    except Exception:
        pass
import store
store.init()
lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None
st.title("Intake Workflow")
if not lead:
    st.info("Select a client in **Client Record** first.")
    st.stop()
name = lead.get("name","")
city = lead.get("city","")
assigned = lead.get("assigned_to") or "Unassigned"
status = (lead.get("status","") or "").replace("_"," ")
budget = lead.get("budget", 0)
budget_str = f"{int(budget):,}" if isinstance(budget,(int,float)) and budget else "—"
timeline = lead.get("timeline","—")
notes = lead.get("notes")
c1, c2, c3, c4 = st.columns([2,1,1,1])
with c1:
    st.caption(name + (" • " + city if city else ""))
    st.caption(f"Assigned: {assigned}")
with c2:
    st.caption("Status"); st.write(status or "—")
with c3:
    st.caption("Budget / mo"); st.write(budget_str)
with c4:
    st.caption("Timeline"); st.write(timeline or "—")
st.divider()
def _ns(key: str) -> str:
    return f"{lead_id}:{key}"
STEP_KEYS = [
    ("Lead received",             "intake_lead_received"),
    ("Lead assigned",             "intake_lead_assigned"),
    ("Initial contact attempted", "intake_first_attempt"),
    ("Initial contact made",      "intake_first_contact"),
    ("Consultation scheduled",    "intake_consult_scheduled"),
    ("Assessment started",        "intake_assessment_started"),
    ("Assessment completed",      "intake_assessment_done"),
    ("Qualification decision",    "intake_qualified"),
]
for _, k in STEP_KEYS:
    st.session_state.setdefault(_ns(k), bool(st.session_state.get(k, False)))
step_done = [bool(st.session_state.get(_ns(k), False)) for _, k in STEP_KEYS]
done_upto   = max([i for i, d in enumerate(step_done) if d] or [-1])
current_idx = (done_upto + 1) if done_upto + 1 < len(STEP_KEYS) else done_upto
st.caption("Intake progress")
st.markdown("""
<style>
.pillrow{display:flex;flex-wrap:wrap;gap:.5rem;margin:8px 0 12px 0}
.pill{font-size:12px; line-height:20px; padding:6px 12px; border-radius:9999px;
  border:1px solid #e5e7eb; background:#f3f4f6; color:#6b7280; user-select:none; white-space:nowrap;}
.pill--done   { background:#e8f2ff; border-color:#93c5fd; color:#1d4ed8; }
.pill--active { background:#dbeafe; border-color:#60a5fa; color:#1e40af; }
.case-card{border:1px solid #e5e7eb; border-radius:12px; padding:12px 16px; background:#fff;}
.muted{color:#6b7280; font-size:12px}
</style>
""", unsafe_allow_html=True)
pills_html = ['<div class="pillrow">']
for i, (label, _) in enumerate(STEP_KEYS):
    cls = "pill"
    if i <= done_upto: cls += " pill--done"
    elif i == current_idx: cls += " pill--active"
    pills_html.append(f'<div class="{cls}">{label}</div>')
pills_html.append('</div>')
st.markdown("".join(pills_html), unsafe_allow_html=True)
completion = (done_upto + 1) / len(STEP_KEYS)
st.progress(completion)
def _sla_for_index(idx: int):
    now = _dt.datetime.utcnow()
    rules = {
        0: ("Lead received", now),
        1: ("Lead assigned", now + _dt.timedelta(hours=24)),
        2: ("Initial contact attempted", now + _dt.timedelta(hours=2)),
        3: ("Initial contact made", now + _dt.timedelta(days=2)),
        4: ("Consultation scheduled", now + _dt.timedelta(days=2)),
        5: ("Assessment started", now + _dt.timedelta(days=3)),
        6: ("Assessment completed", now + _dt.timedelta(days=5)),
        7: ("Qualification decision", now + _dt.timedelta(days=1)),
    }
    return rules.get(idx, ("", now))
step_name, due_ts = _sla_for_index(current_idx if current_idx>=0 else 0)
if step_name:
    st.markdown(f"**Next action:** {step_name} — ✅ On track • **Due:** {due_ts.strftime('%Y-%m-%d %H:%M UTC')}")
st.write("")
lc, rc = st.columns([2,1])
auto_key = _ns("intake_auto_focus_drawer")
if auto_key not in st.session_state: st.session_state[auto_key] = True
def _user_interacted():
    st.session_state[auto_key] = False
with lc:
    for i, (label, key) in enumerate(STEP_KEYS):
        expanded_now = (st.session_state[auto_key] and i == current_idx)
        with st.expander(label, expanded=expanded_now):
            st.checkbox("Mark complete", key=_ns(key), on_change=_user_interacted)
            st.text_area("Notes (optional)", key=_ns(key+":notes"), height=80)
with rc:
    st.markdown("#### Case snapshot")
    st.markdown(f"<div class='case-card'><div class='muted'>{name} • {city}</div>"
                f"<div><span class='muted'>Care preference:</span> {lead.get('preference','—')}</div>"
                f"<div><span class='muted'>Budget:</span> ${budget_str}/mo</div>"
                f"<div><span class='muted'>Timeline:</span> {timeline}</div>"
                f"<div><span class='muted'>Notes:</span> {notes or '—'}</div>"
                f"</div>", unsafe_allow_html=True)
st.write("")
cta1, cta2 = st.columns([1,3])
with cta1:
    if st.button("Complete Intake → Start Placement", type="primary"):
        for _, k in STEP_KEYS:
            st.session_state[_ns(k)] = True
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.experimental_rerun()
with cta2:
    if st.button("← Back to Workflows"):
        st.session_state["_goto_page"] = "pages/89_Workflows.py"
        st.experimental_rerun()
