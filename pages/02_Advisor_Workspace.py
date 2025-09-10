
# 02_Advisor_Workspace.py
import streamlit as st
st.set_page_config(page_title="Advisor Workspace", page_icon="🧰", layout="wide")
from nav_bootstrap import boot; boot()

import store
store.init()

st.title("Advisor Workspace")

# Filters
stage = st.segmented_control("Stage", options=["All","Lead Received","Intake","Case Mgmt"], default="All", key="aw_stage")
origin = st.segmented_control("Origin", options=["All","App","Phone","Hospital"], default="All", key="aw_origin")

leads = store.get_leads()
def match(l):
    ok1 = stage=="All" or l.get("stage")==stage
    ok2 = origin=="All" or l.get("origin")==origin
    return ok1 and ok2
filtered = [l for l in leads if match(l)]

cL, cR = st.columns([0.48,0.52])
with cL:
    st.subheader("Work Queue")
    for l in filtered:
        with st.container(border=True):
            st.write(f"**{l['name']} — {l.get('stage','')}**")
            st.caption(f"{l.get('city','')} • Next: start intake")
            cc1,cc2=st.columns([0.2,0.8])
            with cc1:
                if st.button("View Record Summary", key=f"open_{l['id']}"):
                    store.set_selected_lead(l["id"])
            with cc2:
                if st.button("Client Record", key=f"goto_{l['id']}"):
                    store.set_selected_lead(l["id"])
                    if hasattr(st,"switch_page"): st.switch_page("pages/04_Client_Record.py")

with cR:
    st.subheader("Case Overview")
    lead = store.get_lead(store.get_selected_lead_id()) if store.get_selected_lead_id() else (filtered[0] if filtered else None)
    if not lead:
        st.info("Select a lead on the left.")
    else:
        st.write(f"**{lead['name']} • {lead.get('city','')}**")
        st.caption(f"Stage: {lead.get('stage','')} • Priority: {lead.get('priority','')} • Budget: ${lead.get('budget','')}")
        st.write("Intake progress")
        st.progress(float(lead.get("intake_progress",0.0)))
        st.text_area("Quick note", placeholder="Add a quick note...", key=f"quick_{lead['id']}", height=100)
        st.selectbox("Care needs", ["Choose options","Assistance with ADLs","Memory support"], index=0, key=f"needs_{lead['id']}")
        with st.container(border=True):
            st.subheader("Decision support (last results)")
            st.write(f"**Recommended:** {lead.get('ds_recommendation','—')}")
            st.write(f"**Estimated cost:** ${lead.get('ds_est_cost',0):,} / month")
            if st.button("Open full client record", key=f"full_{lead['id']}"):
                store.set_selected_lead(lead["id"])
                if hasattr(st,"switch_page"): st.switch_page("pages/04_Client_Record.py")
