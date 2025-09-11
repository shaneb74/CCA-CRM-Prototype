# pages/04_Client_Record.py
from __future__ import annotations
import streamlit as st, datetime
try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    try: st.set_page_config(page_title="Case Overview", page_icon="📄", layout="wide")
    except Exception: pass
import store
store.init()
st.title("Case Overview")
leads_all = store.get_leads()
advisors = sorted({l.get("assigned_to") for l in leads_all if l.get("assigned_to")}) or ["Unassigned"]
left, right = st.columns([3,1])
with right:
    st.selectbox("Filter by advisor", ["All advisors"] + advisors, key="client_record_filter_advisor")
q = st.text_input("Search by first or last name", placeholder="Type to filter: e.g., John, Smith, Alvarez", key="client_record_q")
filt_adv = st.session_state.get("client_record_filter_advisor","All advisors")
filtered = []
for l in leads_all:
    if filt_adv != "All advisors" and (l.get("assigned_to") or "Unassigned") != filt_adv: continue
    if q:
        t = (l.get("name","") + " " + l.get("id","")).lower()
        if q.lower() not in t: continue
    filtered.append(l)
if not filtered:
    st.info("No matching clients for the chosen filters."); st.stop()
def _label(l): return f"{l.get('name','')} ({l.get('id','')}) — {l.get('city','')} — {l.get('assigned_to') or 'Unassigned'}"
options = [_label(l) for l in filtered]
default_idx = 0
cur = store.get_selected_lead_id()
if cur:
    for i,l in enumerate(filtered):
        if l.get("id")==cur: default_idx=i; break
sel = st.selectbox("Matching clients", options, index=default_idx, key="client_record_match_select")
lead = filtered[options.index(sel)]
store.set_selected_lead(lead.get("id"))
st.session_state["_lead_obj"] = lead
origin = lead.get("origin","App")
created_on = datetime.date.today().isoformat()
st.success(f"Origin: {str(origin).title()} — Guided Care Plan completed on {created_on}")
c1,c2,c3,c4 = st.columns([2,1,1,1])
with c1: st.subheader(lead.get("name","")); st.caption(lead.get("city",""))
with c2: st.caption("Status"); st.write(lead.get("status","New"))
with c3: st.caption("Assigned"); st.write(lead.get("assigned_to") or "Unassigned")
with c4: st.caption("Lead ID"); st.write(lead.get("id","—"))
st.divider()
st.subheader("Decision Support")
dsr = lead.get("ds_recommendation") or lead.get("preference") or "—"
dsc = lead.get("ds_est_cost")
cost_str = f"${int(dsc):,} / month" if isinstance(dsc,(int,float)) and dsc>0 else "—"
st.write(f"**Recommended:** {dsr}")
st.write(f"**Estimated cost:** {cost_str}")
btns = st.columns([1,1,1,6])
def _assign_to_me():
    me = getattr(store,"CURRENT_USER","Current Advisor")
    if lead.get("assigned_to") != me:
        lead["assigned_to"] = me; store.upsert_lead(lead); st.success(f"Assigned to {me}"); st.experimental_rerun()
with btns[0]:
    me = getattr(store,"CURRENT_USER","Current Advisor")
    st.button("Assign to me", on_click=_assign_to_me, disabled=(lead.get("assigned_to")==me), key="assign_to_me_btn")
def _go_intake():
    store.set_selected_lead(lead["id"]); st.session_state["_goto_page"] = "pages/90_Intake_Workflow.py"; st.experimental_rerun()
with btns[1]:
    st.button("Start Intake", on_click=_go_intake, key="start_intake_btn")
def _go_place():
    store.set_selected_lead(lead["id"]); st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"; st.experimental_rerun()
with btns[2]:
    st.button("Open Placement Workflow", on_click=_go_place, key="open_placement_btn")
