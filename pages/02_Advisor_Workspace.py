
from ui_chrome import apply_chrome
import store
import streamlit as st
apply_chrome()
store.init()

st.title("Advisor Workspace")

# Filters
st.caption("Filter")
flt = st.radio("", options=["All leads","App","Phone","Hospital"], horizontal=True, index=0, label_visibility="collapsed")

# Work Queue
st.subheader("Work Queue")
for l in store.get_leads()[:3]:
    with st.container(border=True):
        st.write(f"**{l['name']} — Intake**")
        st.caption(f"{l['city']} • Next: start intake")
        cols = st.columns([1,1])
        with cols[0]:
            if st.button("Open", key=f"aw_open_{l['id']}"):
                store.set_selected_lead(l['id'])
                st.session_state["_goto_page"]="pages/04_Client_Record.py"
                st.experimental_rerun()
        with cols[1]:
            if st.button("Client Record", key=f"aw_cr_{l['id']}"):
                store.set_selected_lead(l['id'])
                st.session_state["_goto_page"]="pages/04_Client_Record.py"
                st.experimental_rerun()

# Case Overview (right-side style, single lead preview)
st.subheader("Case Overview")
lead = store.get_leads()[0]
st.caption(f"{lead['name']} • {lead['city']}")
st.progress(min(1.0, max(0.0, float(lead.get('progress',0)))))
st.text_area("Quick note", placeholder="Add a quick note...", height=100)
st.selectbox("Care needs", options=["Assistance with ADLs","Memory support","Skilled nursing"], index=0)

# Decision support + actions
st.subheader("Decision support (last results)")
st.write(f"**Recommended:** {lead.get('ds_recommendation','Assisted Living')}")
st.write(f"**Estimated cost:** ${int(lead.get('ds_est_cost',4500)):,} / month")

btns = st.columns(3)
with btns[0]:
    st.button("Open full client record", key="aw_open_full", on_click=lambda: st.session_state.update(**{"_goto_page":"pages/04_Client_Record.py"}))
with btns[1]:
    st.button("Start Intake", key="aw_start_intake", on_click=lambda: st.session_state.update(**{"_goto_page":"pages/90_Intake_Workflow.py"}))
with btns[2]:
    st.button("Open Placement Workflow", key="aw_open_place", on_click=lambda: st.session_state.update(**{"_goto_page":"pages/91_Placement_Workflow.py"}))
