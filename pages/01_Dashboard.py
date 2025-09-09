
import streamlit as st
from ui.widgets import inject_css, kpi_band, kpi, banner, card, pills_row

inject_css()
st.title("Advisor Dashboard")

with kpi_band("At a glance"):
    col1, col2, col3, col4 = st.columns([1,1,1,1.2])
    with col1:
        kpi("New leads (today)", "5", "+2 vs yesterday", "green")
    with col2:
        kpi("Assigned leads", "12", "+1 this week", "green")
    with col3:
        kpi("Active cases", "3", "-1 since Fri", "red")
    with col4:
        st.markdown("#### MTD vs goal")
        st.markdown("### $20,500 / $40,000")
        pills_row([("51% of goal","gray")])

banner("Upload signed Disclosure before scheduling tours.  [Compliance]", "info", show_close=True)
banner("Confirm Medicaid rollover during financial review.  [Financial]", "info", show_close=True)
banner("Keep intake notes date-stamped with initials.  [General]", "info", show_close=True)

left, right = st.columns([1,1])
with left:
    with card("Tasks & Queues"):
        tasks = ["Call lead John Doe", "Follow up with client Jane", "Prepare intake forms",
                 "Schedule case review", "Complete assessment for Mary Johnson"]
        for t in tasks:
            st.checkbox(t, value=False)
    with card("Communications"):
        st.write("[Referral] Harborview MC — Disclosure still pending.")
    with card("Pipeline by Workflow Stage"):
        st.progress(0.62)
with right:
    st.subheader("Advisor Workflows")
    with card("Lead → Intake"):
        with card("Lead Received"):
            st.caption("Call client and start intake (~30 min). Upload disclosure before tours.")
        with card("Client Intake"):
            st.caption("Complete intake in CRM. Keep notes date-stamped.")
    with card("Case Management → Search"):
        with card("Case Management"):
            st.caption("Discuss barriers, discharge date, log contact.")
    with card("Decision → Transition → Invoice"):
        with card("Financial Review"):
            st.caption("Discuss Medicaid rollover, budget. Log in CRM.")
