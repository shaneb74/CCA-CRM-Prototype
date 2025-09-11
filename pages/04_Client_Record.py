# pages/04_Client_Record.py
from __future__ import annotations
import streamlit as st, datetime
try:
    import store
except Exception:
    store=None
try:
    st.set_page_config(page_title="Case Overview", page_icon="📄", layout="wide")
except Exception:
    pass
def _go_intake_from_record():
    lead=st.session_state.get("_lead_obj"); lead_id=lead.get("id") if isinstance(lead,dict) else None
    if lead_id and store: 
        try: store.set_selected_lead(lead_id)
        except Exception: pass
    try:
        if hasattr(st,"switch_page"): st.switch_page("pages/90_Intake_Workflow.py"); return
    except Exception: pass
    st.session_state["_goto_page"]="pages/90_Intake_Workflow.py"; st.experimental_rerun()
if store:
    try: store.init()
    except Exception: pass
st.title("Case Overview")
leads=[]
if store:
    try: leads=store.get_leads()
    except Exception: pass
if not leads:
    st.info("No leads available. Add a lead to begin."); st.stop()
lead_id_current=store.get_selected_lead_id() if store else None
options=[f"{l.get('name','')} ({l.get('id','')}) — {l.get('city','')}" for l in leads]
idx_default=0
if lead_id_current:
    for i,l in enumerate(leads):
        if l.get('id')==lead_id_current: idx_default=i; break
sel=st.selectbox("Matching clients", options=options, index=idx_default, key="client_record_match_select")
selected=leads[options.index(sel)]
if store:
    try: store.set_selected_lead(selected.get("id"))
    except Exception: pass
lead=selected; st.session_state["_lead_obj"]=lead
origin=lead.get("origin","App"); created_on=datetime.date.today().isoformat()
st.success(f"Origin: {str(origin).title()} — Guided Care Plan completed on {created_on}")
c1,c2,c3,c4=st.columns([2,1,1,1])
with c1: st.subheader(lead.get("name","")); st.caption(lead.get("city",""))
with c2: st.caption("Status"); st.write(str(lead.get("status","New")).replace("_"," ").title())
with c3: st.caption("Assigned"); st.write(lead.get("assigned_to") or "Unassigned")
with c4: st.caption("Lead ID"); st.write(lead.get("id","—"))
st.divider()
lc1,lc2=st.columns([2,2])
with lc1:
    st.subheader("Info from App")
    st.write(f"**Care Preference:** {lead.get('preference','—')}")
    budget=lead.get("budget",0); st.write(f"**Budget:** {'${:,}/month'.format(int(budget)) if budget else '—'}")
    st.write(f"**Timeline:** {lead.get('timeline','—')}")
    if lead.get("notes"): st.write(f"**Notes:** {lead.get('notes')}")
with lc2:
    st.subheader("Next Steps")
    st.checkbox(f"Call {lead.get('name','client')} within 24h", key="ns_call", value=False)
    st.checkbox("Upload Disclosure", key="ns_disclosure", value=False)
    st.checkbox("Complete Intake", key="ns_intake", value=False)
st.divider()
st.subheader("Decision Support")
dsr=lead.get("ds_recommendation") or lead.get("preference") or "—"
dsc=lead.get("ds_est_cost")
cost_str=f"${int(dsc):,} / month" if isinstance(dsc,(int,float)) and dsc>0 else "—"
st.write(f"**Recommended:** {dsr}"); st.write(f"**Estimated cost:** {cost_str}")
btns=st.columns([1,1,1,6])
me=(getattr(store,"CURRENT_USER","Current Advisor") if store else "Current Advisor")
already_mine=(lead.get("assigned_to")==me)
with btns[0]:
    def _assign():
        if not store: return
        m=getattr(store,"CURRENT_USER","Current Advisor")
        if lead.get("assigned_to")!=m:
            lead["assigned_to"]=m; store.upsert_lead(lead); st.success(f"Assigned to {m}"); st.experimental_rerun()
    st.button("Assign to me", on_click=_assign, disabled=already_mine, key="assign_to_me_btn")
with btns[1]:
    st.button("Start Intake", on_click=_go_intake_from_record, disabled=not already_mine, key="start_intake_btn")
with btns[2]:
    def _open_place():
        if store and lead.get("id"): store.set_selected_lead(lead["id"])
        st.session_state["_goto_page"]="pages/91_Placement_Workflow.py"; st.experimental_rerun()
    st.button("Open Placement Workflow", on_click=_open_place, key="open_placement_btn")
st.caption("After tours, log results here and the pipeline will advance automatically.")
