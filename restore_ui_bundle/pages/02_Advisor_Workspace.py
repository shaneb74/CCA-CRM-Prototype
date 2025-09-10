
# pages/02_Advisor_Workspace.py — restored split view (queue + case overview)
import streamlit as st
import store
from ui_chrome import apply_chrome

apply_chrome("Advisor Workspace", "🧰")
store.init()

st.title("Advisor Workspace")

# Filters
st.caption("Filter")
fcol = st.columns([1,1,1,1,1])
lead_source = fcol[0].radio(" ", ["All leads","App","Phone","Hospital"], horizontal=True, label_visibility="collapsed")
st.caption("Stage")
stage = st.radio("stage", ["All","Lead Received","Intake","Case Mgmt"], horizontal=True, label_visibility="collapsed", key="ws_stage")

leads = store.get_leads()

# Work Queue list
st.subheader("Work Queue")
queue_col, detail_col = st.columns((6,7))

def _item_card(l):
    with st.container(border=True):
        st.write(f"**{l.get('name')} — {l.get('status','Intake').title()}**")
        st.caption(f"{l.get('city','')} • Next: start intake")
        cols = st.columns([1,1])
        with cols[0]:
            if st.button("Open", key=f"open_{l['id']}"):
                store.set_selected_lead(l["id"])
        with cols[1]:
            if st.button("Client Record", key=f"rec_{l['id']}"):
                store.set_selected_lead(l["id"])
                st.session_state["_goto_page"] = "pages/04_Client_Record.py"
                st.experimental_rerun()

with queue_col:
    for l in leads[:6]:
        _item_card(l)

# Case Overview summary (right)
sel_id = store.get_selected_lead_id() or (leads[0]["id"] if leads else None)
lead = store.get_lead(sel_id) if sel_id else None

with detail_col:
    st.subheader("Case Overview")
    if not lead:
        st.info("Select a lead from the list to view summary.")
    else:
        st.write(f"**{lead.get('name')} • {lead.get('city','')}**")
        st.caption(f"Stage: Intake • Priority: 2 • Budget: ${lead.get('budget',0)}")
        st.text_area("Quick note", placeholder="Add a quick note...", key="ws_note")
        st.caption("Intake progress")
        st.progress(min(max(float(lead.get('progress',0.0)),0.0),1.0))
        st.selectbox("Care needs", ["Choose options","Assistance with ADLs","Memory care"], index=0)
        st.subheader("Decision support (last results)")
        st.info(f"Recommended: {lead.get('ds_recommendation','Assisted Living')}\n\nEstimated cost: ${int(lead.get('ds_est_cost') or 0):,} / month")
        st.button("Open full client record",
                  on_click=lambda: st.session_state.update(_goto_page="pages/04_Client_Record.py"))

