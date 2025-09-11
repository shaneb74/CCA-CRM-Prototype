# pages/04_Client_Record.py  (patched redirect logic only)
from __future__ import annotations
import streamlit as st
import datetime
import store

# --- Helpers ----
def _switch_or_schedule(path: str):
    """Prefer switch_page in the main run (not a callback)."""
    if hasattr(st, "switch_page"):
        try:
            st.switch_page(path)
            return
        except Exception:
            pass
    st.session_state["_goto_page"] = path
    # safe to rerun here (we are NOT inside on_click callback)
    try:
        st.rerun()
    except Exception:
        pass

st.set_page_config(page_title="Case Overview", page_icon="📄", layout="wide")
store.init()

st.title("Case Overview")

leads = store.get_leads()

def _lead_label(l: dict) -> str:
    return f"{l.get('name','')} ({l.get('id','')}) — {l.get('city','')} — {l.get('assigned_to') or 'Unassigned'}"

lead_id_current = store.get_selected_lead_id()
options = [_lead_label(l) for l in leads]
idx_default = 0
if lead_id_current:
    for i,l in enumerate(leads):
        if l.get('id') == lead_id_current:
            idx_default = i
            break

sel = st.selectbox("Matching clients", options=options, index=idx_default, key="client_record_match_select")
lead = leads[options.index(sel)] if leads else None
if lead:
    store.set_selected_lead(lead.get("id"))

if not lead:
    st.info("No clients found.")
    st.stop()

origin = lead.get("origin", "App")
created_on = datetime.date.today().isoformat()
st.success(f"Origin: {str(origin).title()} — Guided Care Plan completed on {created_on}")

c1,c2,c3,c4 = st.columns([2,1,1,1])
with c1:
    st.subheader(lead.get("name",""))
    st.caption(lead.get("city",""))
with c2:
    st.caption("Status"); st.write(lead.get("status","New"))
with c3:
    st.caption("Assigned"); st.write(lead.get("assigned_to") or "Unassigned")
with c4:
    st.caption("Lead ID"); st.write(lead.get("id","—"))

st.divider()

# Decision support preview
st.subheader("Decision Support")
dsr = lead.get("ds_recommendation") or lead.get("preference") or "—"
dsc = lead.get("ds_est_cost")
cost_str = f"${int(dsc):,} / month" if isinstance(dsc,(int,float)) and dsc>0 else "—"
st.write(f"**Recommended:** {dsr}"); st.write(f"**Estimated cost:** {cost_str}")

b1,b2,b3,_ = st.columns([1,1,1,6])
me = getattr(store, "CURRENT_USER", "Current Advisor")
already_mine = (lead.get("assigned_to") == me)

with b1:
    if st.button("Assign to me", disabled=already_mine, key="assign_to_me_btn"):
        if lead.get("assigned_to") != me:
            lead["assigned_to"] = me
            store.upsert_lead(lead)
            st.success(f"Assigned to {me}")
            st.rerun()

with b2:
    if st.button("Start Intake", disabled=not already_mine, key="start_intake_btn_main"):
        # inline button handling (not on_click) => safe to rerun/switch
        if lead and lead.get("id"):
            store.set_selected_lead(lead["id"])
        # prefer 90_* if present
        for dest in ("pages/90_Intake_Workflow.py", "pages/06_Intake_Workflow.py"):
            _switch_or_schedule(dest)
        st.stop()

with b3:
    if st.button("Open Placement Workflow", key="open_placement_btn_main"):
        if lead and lead.get("id"):
            store.set_selected_lead(lead["id"])
        _switch_or_schedule("pages/91_Placement_Workflow.py")
        st.stop()

st.caption("After tours, log results here and the pipeline will advance automatically.")