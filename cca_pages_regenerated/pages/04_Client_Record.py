from ui_chrome import apply_chrome
apply_chrome()

import streamlit as st, datetime
import store

store.init()
st.title("Case Overview")

# filters
leads = store.get_leads()
advisors = sorted({l.get("assigned_to") for l in leads if l.get("assigned_to")}) or ["Unassigned"]
advisor_filter = st.selectbox("Filter by advisor", ["All advisors"] + advisors, index=0)

q = st.text_input("Search by first or last name", placeholder="Type to filter: e.g., John, Smith, Alvarez")

def _label(l): 
    return f"{l.get('name','')} ({l.get('id','')}) — {l.get('city','')} — {l.get('assigned_to') or 'Unassigned'}"

filtered = []
for l in leads:
    if advisor_filter != "All advisors" and (l.get("assigned_to") or "Unassigned") != advisor_filter:
        continue
    if q and (q.lower() not in l.get("name","").lower() and q.lower() not in l.get("id","").lower()):
        continue
    filtered.append(l)
if not filtered and not q and advisor_filter=="All advisors":
    filtered = leads

lead_id_current = store.get_selected_lead_id()
options = [_label(l) for l in filtered] or ["— no clients —"]
idx = 0
if lead_id_current:
    for i,l in enumerate(filtered):
        if l.get("id")==lead_id_current: idx=i; break

sel = st.selectbox("Matching clients", options, index=idx)
if filtered:
    selected = filtered[options.index(sel)]
    store.set_selected_lead(selected.get("id"))

lead = store.get_lead(store.get_selected_lead_id()) if store.get_selected_lead_id() else (filtered[0] if filtered else None)
st.session_state["_lead_obj"] = lead

if not lead:
    st.info("No matching clients. Adjust filters above.")
    st.stop()

created_on = datetime.date.today().isoformat()
st.success(f"Origin: {str(lead.get('origin','App')).title()} — Guided Care Plan completed on {created_on}")

c1,c2,c3,c4 = st.columns([2,1,1,1])
with c1:
    st.subheader(lead.get("name","")); st.caption(lead.get("city",""))
with c2:
    st.caption("Status"); st.write(lead.get("status","New"))
with c3:
    st.caption("Assigned"); st.write(lead.get("assigned_to") or "Unassigned")
with c4:
    st.caption("Lead ID"); st.write(lead.get("id","—"))

st.divider()
lc1, lc2 = st.columns([2,2])
with lc1:
    st.subheader("Info from App")
    st.write(f"**Care Preference:** {lead.get('preference','—')}")
    budget = lead.get("budget",0)
    st.write(f"**Budget:** {'$'+format(int(budget),',')+'/month' if budget else '—'}")
    st.write(f"**Timeline:** {lead.get('timeline','—')}")
    if lead.get("notes"): st.write(f"**Notes:** {lead['notes']}")

with lc2:
    st.subheader("Next Steps")
    st.checkbox(f"Call {lead.get('name','client')} within 24h", key="ns_call")
    st.checkbox("Upload Disclosure", key="ns_disclosure")
    st.checkbox("Complete Intake", key="ns_intake")

st.divider()
st.subheader("Decision Support")
dsr = lead.get("ds_recommendation") or lead.get("preference") or "—"
dsc = lead.get("ds_est_cost")
cost_str = f"${int(dsc):,} / month" if isinstance(dsc,(int,float)) and dsc>0 else "—"
st.write(f"**Recommended:** {dsr}")
st.write(f"**Estimated cost:** {cost_str}")

me = getattr(store, "CURRENT_USER", "Current Advisor")
already_mine = (lead.get("assigned_to")==me)
b1,b2,b3,_ = st.columns([1,1,2,6])

def _assign_to_me():
    if lead.get("assigned_to")!=me:
        lead["assigned_to"]=me
        store.upsert_lead(lead)
        st.success(f"Assigned to {me}")
        st.experimental_rerun()

with b1:
    st.button("Assign to me", on_click=_assign_to_me, disabled=already_mine, key="assign_to_me_btn")
with b2:
    if st.button("Start Intake", disabled=not already_mine, key="start_intake_btn"):
        st.session_state["_goto_page"]="pages/90_Intake_Workflow.py"
        st.experimental_rerun()
with b3:
    if st.button("Open Placement Workflow", key="open_placement_btn"):
        st.session_state["_goto_page"]="pages/91_Placement_Workflow.py"
        st.experimental_rerun()

st.caption("After tours, log results here and the pipeline will advance automatically.")
