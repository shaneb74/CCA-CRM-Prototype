from ui_chrome import apply_chrome
apply_chrome()

import streamlit as st
from datetime import date, timedelta
import store

store.init()
st.title("Advisor Dashboard")

leads = store.get_leads()
today = date.today()

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.metric("New leads (today)", len(leads), "+2 vs yesterday")
with c2:
    st.metric("Assigned leads", len([l for l in leads if l.get("assigned_to")]), "+1 this week")
with c3:
    st.metric("Active cases", len(leads), "-1 since Fri")
with c4:
    st.metric("MTD vs goal", "$20,500 / $40,000", "51% of goal")

with st.expander("Guidance & Alerts", expanded=False):
    st.write("- Upload signed Disclosure before scheduling tours.")
    st.write("- Confirm Medicaid rollover during financial review.")
    st.write("- Keep intake notes date-stamped with initials.")

st.subheader("Tasks & Queues")
left, right = st.columns(2)
with left:
    st.caption("Due today")
    st.write("• Call John Doe")
    st.write("• Upload Disclosure for John Doe")
    st.write("• Call Mary Smith")
with right:
    st.caption("Upcoming")
    st.write("• Complete intake for Luis Alvarez")

st.divider()
st.subheader("Advisor Workflows")
if st.button("Open Workflows hub →"):
    st.session_state["_goto_page"] = "pages/89_Workflows.py"
    st.experimental_rerun()
