
# pages/01_Dashboard.py — restored cards, alerts drawer, tasks, advisor workflows
import streamlit as st
from datetime import date, timedelta
import store
from ui_chrome import apply_chrome

apply_chrome("Advisor Dashboard", "📊")
store.init()

st.title("Advisor Dashboard")

# --- KPI cards ---
k1, k2, k3, k4 = st.columns(4)
leads = store.get_leads()
assigned = [l for l in leads if l.get("assigned_to")]
active = [l for l in leads if l.get("status","").lower() in ("in_progress","in progress")]
with k1:
    st.metric("New leads (today)", 2, "+2 vs yesterday")
with k2:
    st.metric("Assigned leads", len(assigned), "+1 this week")
with k3:
    st.metric("Active cases", len(active), "-1 since Fri")
with k4:
    st.metric("MTD vs goal", "$20,500 / $40,000", "51% of goal")

# --- Guidance & Alerts drawer (starts closed, shows badge if new) ---
with st.expander("Guidance & Alerts  🔔 3 new", expanded=False):
    st.write("Upload signed Disclosure before scheduling tours.")
    st.write("Confirm Medicaid rollover during financial review.")
    st.write("Keep intake notes date-stamped with initials.")

# --- Tasks & Queues ---
st.subheader("Tasks & Queues • Today: 2 • Upcoming: 3")
left, right = st.columns((7,5))

with left:
    st.caption("Due today")
    for t in store.get_tasks():
        with st.container(border=True):
            st.write(f"**{t.get('title')}**")
            colA, colB = st.columns([5,1])
            with colA:
                st.caption(f"Due {t.get('due')}")
            with colB:
                if st.button("✓ Complete", key=f"done_{t['id']}"):
                    store.complete_task(t['id'])
                    st.experimental_rerun()

    st.write("Add quick task")
    title = st.text_input("Task title", key="quick_task")
    pri = st.selectbox("Priority", ["Low", "Med", "High"], index=1, key="quick_task_pri")
    if st.button("Add", key="add_quick"):
        store.add_task({"id": f"T-new-{len(store.get_tasks(False))+1}", "title": title or "Untitled", "done": False, "priority": pri, "due": date.today()})
        st.experimental_rerun()

with right:
    st.caption("Upcoming")
    with st.container(border=True):
        st.write("**Complete intake for Luis Alvarez**")
        st.caption("Due 2025-09-11")
        st.button("✓ Complete", key="u1")

    st.write("Add task (upcoming)")
    st.text_input("Task title", key="up_title")
    st.selectbox("Priority", ["Low","Med","High"], index=0, key="up_pri")
    st.text_input("Due date", value=str(date.today()+timedelta(days=1)), key="up_due")
    st.button("Add", key="up_add")

st.divider()

# --- Communications placeholder ---
with st.expander("Communications", expanded=False):
    st.caption("Recent messages and calls show here.")

# --- Advisor Workflows (hub buttons) ---
with st.expander("Advisor Workflows", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Open Workflows hub →", key="to_hub"):
            st.session_state["_goto_page"] = "pages/89_Workflows.py"
            st.experimental_rerun()
    with c2:
        st.button("Open Intake →", key="to_intake",
                  on_click=lambda: st.session_state.update(_goto_page="pages/90_Intake_Workflow.py"))
    with c3:
        st.button("Open Placement →", key="to_place",
                  on_click=lambda: st.session_state.update(_goto_page="pages/91_Placement_Workflow.py"))
