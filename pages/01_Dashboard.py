
# 01_Dashboard.py
import streamlit as st
st.set_page_config(page_title="Advisor Dashboard", page_icon="📊", layout="wide")
from nav_bootstrap import boot; boot()

import store
store.init()

st.title("Advisor Dashboard")

leads = store.get_leads()
new_today = sum(1 for l in leads if l.get("origin","").lower().startswith("app"))
assigned = sum(1 for l in leads if l.get("assigned_to"))
active = sum(1 for l in leads if l.get("stage") in ("Lead Received","Intake","Case Mgmt"))

c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("New leads (today)", new_today, "+ from app and other sources")
with c2: st.metric("Assigned leads", assigned, "+ this week")
with c3: st.metric("Active cases", active, "- since Fri")
with c4: st.metric("MTD vs goal", "$20,500 / $40,000", "51% of goal")

st.subheader("Guidance & Alerts")
with st.expander("Show alerts", expanded=False):
    st.info("Upload signed Disclosure before scheduling tours.  
Confirm Medicaid rollover during financial review.  
Keep intake notes date-stamped with initials.")

st.subheader("Tasks & Queues")
with st.container(border=True):
    cL, cR = st.columns(2)
    with cL:
        st.caption("Due today")
        for t in store.get_demo_tasks("today"):
            with st.container(border=True):
                st.write(f"**{t['title']}**")
                st.caption(f"Due {t['due']}"); st.button("✓ Complete", key=f"done_{t['id']}")
        with st.form("quick_add_today", clear_on_submit=True):
            st.text_input("Add quick task", key="q_task_today")
            st.selectbox("Priority", ["High","Med","Low"], index=1, key="q_prio_today")
            st.form_submit_button("Add")
    with cR:
        st.caption("Upcoming")
        for t in store.get_demo_tasks("upcoming"):
            with st.container(border=True):
                st.write(f"**{t['title']}**")
                st.caption(f"Due {t['due']}"); st.button("✓ Complete", key=f"done2_{t['id']}")

st.subheader("Pipeline by Workflow Stage")
st.progress(0.64)

with st.expander("Communications"):
    st.write("Recent messages and call summaries will show here.")

st.subheader("Advisor Workflows")
with st.expander("Lead → Intake • Case Mgmt • Decision → Transition • Invoice", expanded=False):
    if hasattr(st, "page_link"):
        st.page_link("pages/00_Workflows.py", label="Open Workflows →")
        st.page_link("pages/06_Intake_Workflow.py", label="Open Intake →")
        st.page_link("pages/07_Placement_Workflow.py", label="Open Placement →")
        st.page_link("pages/08_Followup_Workflow.py", label="Open Follow-up →")
