
from ui_chrome import apply_chrome
import store
import streamlit as st
apply_chrome()
store.init()

from datetime import date

st.title("Advisor Dashboard")

# Stats row
c1, c2, c3, c4 = st.columns(4)
leads = store.get_leads()
tasks = store.get_tasks()
with c1:
    st.metric("New leads (today)", 2, "+2 vs yesterday")
with c2:
    st.metric("Assigned leads", len([l for l in leads if l.get("assigned_to")==store.CURRENT_USER]), "+1 this week")
with c3:
    st.metric("Active cases", len([l for l in leads if l.get("status")!='new']), "-1 since Fri")
with c4:
    st.metric("MTD vs goal", "$20,500 / $40,000", "51% of goal")

# Guidance & Alerts (drawer style)
with st.expander(f"Guidance & Alerts  🔔 {len(store.get_notifications())} new", expanded=False):
    for n in store.get_notifications():
        st.write("-", n["text"])

st.markdown("---")

# Tasks & Queues (left) / Upcoming (right)
left, right = st.columns([2,1])
with left:
    st.caption("Tasks & Queues • Today")
    for t in tasks:
        with st.container(border=True):
            st.write(t["title"])
            st.caption(f"Due {t['due']}")
            st.button("✓ Complete", key=f"complete_{t['id']}", use_container_width=False)

    with st.container(border=True):
        st.caption("Add quick task")
        st.text_input("Title", key="dash_quick_task_title", label_visibility="collapsed", placeholder="Add task")
        st.selectbox("Priority", options=["High","Med","Low"], index=1, key="dash_quick_task_pri", label_visibility="collapsed")
        st.button("Add")

with right:
    st.caption("Upcoming")
    with st.container(border=True):
        st.write("Complete intake for Luis Alvarez")
        st.caption("Due " + str(date.today()))
        st.button("✓ Complete", key="complete_upcoming")
