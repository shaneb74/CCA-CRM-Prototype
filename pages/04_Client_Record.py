
# 04_Client_Record.py
import streamlit as st
st.set_page_config(page_title="Case Overview", page_icon="🗂️", layout="wide")
from nav_bootstrap import boot; boot()

import store
store.init()

st.title("Case Overview")

# Filters/search
advisors = ["All advisors"] + sorted({l.get("assigned_to","Unassigned") or "Unassigned" for l in store.get_leads()})
adv = st.selectbox("Filter by advisor", advisors, index=0, key="cr_adv")
query = st.text_input("Search by first or last name", placeholder="Type to filter: e.g., John, Smith, Alvarez", key="cr_q")

def visible(l):
    ok_adv = adv=="All advisors" or (l.get("assigned_to") or "Unassigned")==adv
    ok_q = (query.strip().lower() in l["name"].lower()) if query.strip() else True
    return ok_adv and ok_q

matches = [l for l in store.get_leads() if visible(l)]
lead_names = [f"{l['name']} ({l['id']}) — {l.get('city','')}" for l in matches] or ["—"]
sel = st.selectbox("Matching clients", lead_names, index=0)
lead = matches[lead_names.index(sel)] if matches else None

if lead:
    store.set_selected_lead(lead["id"])
    st.success(f"Origin: {lead.get('origin','')} — Guided Care Plan completed on 2025-09-10")
    c1,c2,c3 = st.columns([0.4,0.3,0.3])
    with c1:
        st.subheader(lead["name"]); st.caption(lead.get("city",""))
    with c2:
        st.caption(f"Status: {lead.get('status','New')}")
        st.caption(f"Assigned: {lead.get('assigned_to') or 'Unassigned'}")
    with c3:
        st.caption(f"Lead ID: {lead['id']}")

    st.subheader("Info from App")
    c1,c2 = st.columns(2)
    with c1:
        st.write(f"**Care Preference:** {lead.get('ds_recommendation','—')}")
        st.write(f"**Budget:** ${lead.get('budget','—')}/month")
        st.write(f"**Timeline:** {lead.get('timeline','—')}")
        st.write(f"**Notes:** {lead.get('notes','—')}")
    with c2:
        st.subheader("Next Steps")
        st.checkbox(f"Call {lead['name']} within 24h", key=f"ns1_{lead['id']}")
        st.checkbox("Upload Disclosure", key=f"ns2_{lead['id']}")
        st.checkbox("Complete Intake", key=f"ns3_{lead['id']}")

    st.subheader("Decision Support")
    st.write(f"**Recommended:** {lead.get('ds_recommendation','—')}")
    st.write(f"**Estimated cost:** ${lead.get('ds_est_cost',0):,} / month")

    me = (lead.get("assigned_to") or "").strip().lower() == (store.CURRENT_USER or "").strip().lower()
    already_assigned = bool(lead.get("assigned_to"))
    # Assign to me button enabled only if unassigned
    st.button("Assign to me", key=f"assign_{lead['id']}", disabled=already_assigned, on_click=lambda: store.assign_to_current(lead["id"]))
    # Start Intake enabled only if assigned to me
    start_disabled = not me
    if st.button("Start Intake", disabled=start_disabled, key=f"start_{lead['id']}"):
        st.session_state["intake_lead_id"] = lead["id"]
        st.toast("Intake started")
        if hasattr(st,"switch_page"): st.switch_page("pages/06_Intake_Workflow.py")
