
# pages/90_Intake_Workflow.py
from __future__ import annotations
import streamlit as st
from datetime import datetime
import intake_store as ixs
import store

# ----- safe reroute consumer (works with/without ui_chrome) -----
def _consume_redirect_once():
    k = "_goto_page"
    dest = st.session_state.pop(k, None)
    if dest and hasattr(st, "switch_page"):
        try:
            st.switch_page(dest)
        except Exception:
            pass

st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
_consume_redirect_once()

store.init()
lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")

if not lead:
    st.info("No client selected. Use Client Record or the Workflows hub.")
    st.stop()

# Ensure intake state & meta stored centrally
ixs.init_for_lead(lead)
meta = ixs.get_meta(lead["id"])

# ---- Header snapshot (compact) ----
snap_cols = st.columns([2,1,1,1])
with snap_cols[0]:
    st.markdown(f"**{lead.get('name','')}** • {lead.get('city','')}")
    st.caption(f"Assigned: {lead.get('assigned_to') or 'Unassigned'}")
with snap_cols[1]:
    st.caption("Status")
    st.write(lead.get("status","—"))
with snap_cols[2]:
    st.caption("Budget / mo")
    val = lead.get("budget")
    st.write(f"{val:,}" if isinstance(val,(int,float)) and val>0 else "—")
with snap_cols[3]:
    st.caption("Timeline")
    st.write(lead.get("timeline","—"))

# Origin + received
o = meta.get("origin","Unknown")
try:
    ra = datetime.fromisoformat(meta.get("received_at"))
except Exception:
    ra = None

top_info = st.columns([1,1,6])
with top_info[0]:
    st.info(f"Origin: {str(o)}")
with top_info[1]:
    st.info(f"Received: {ixs.human_when(ra) if ra else '—'}")

st.divider()

# ---- Pills (horizontal) ----
state = ixs.get_state(lead["id"])
pill_cols = st.columns(8)
for i, step in enumerate(ixs.STEP_ORDER):
    label = ixs.STEP_LABELS[step]
    with pill_cols[i]:
        if state.get(step,{}).get("done"):
            st.button(label, key=f"pill_{step}", disabled=True)
        else:
            st.button(label, key=f"pill_{step}", disabled=True)

# Next action + SLA
nxt, due, status = ixs.sla_status(lead["id"])
if nxt:
    badge = {"ok":"✅ On track","due_soon":"⏳ Due soon","overdue":"⚠️ Overdue"}[status]
    due_str = due.strftime("%Y-%m-%d %H:%M UTC") if due else "—"
    st.markdown(f"**Next action:** {ixs.STEP_LABELS[nxt]} • {badge} • **Due:** {due_str}")

st.progress(ixs.percent_complete(lead["id"]))

st.write("")

# ---- Two-column content: drawers (left) + case snapshot (right) ----
left, right = st.columns([3,2], gap="large")

with left:
    # No drawer for lead_received (info is shown above)
    for step in ixs.STEP_ORDER:
        if step == "lead_received":
            continue
        label = ixs.STEP_LABELS[step]
        with st.expander(label, expanded=False):
            # Basic "done" toggle
            done = state.get(step,{}).get("done", False)
            new_done = st.checkbox("Mark as complete", value=done, key=f"chk_{step}")
            if new_done and not done:
                ixs.mark_step(lead["id"], step, True)
                st.success("Saved")
                st.experimental_rerun()
            # Simple notes field per step (kept in session for demo)
            notes_key = f"notes::{lead['id']}::{step}"
            st.text_area("Notes (optional)", key=notes_key)

    st.write("")
    if st.button("Complete Intake → Start Placement", type="primary"):
        ixs.mark_step(lead["id"], "qualification_decision", True)
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.experimental_rerun()

    st.button("← Back to Workflows", on_click=lambda: st.session_state.update({"_goto_page":"pages/89_Workflows.py"}))

with right:
    st.subheader("Case snapshot")
    st.caption(f"{lead.get('name','')} • {lead.get('city','')} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")
    if lead.get("preference"):
        st.write(f"**Care preference:** {lead['preference']}")
    if lead.get("budget"):
        st.write(f"**Budget:** ${int(lead['budget']):,}/mo")
    if lead.get("timeline"):
        st.write(f"**Timeline:** {lead['timeline']}")
    if lead.get("notes"):
        st.write(f"**Notes:** {lead['notes']}")
