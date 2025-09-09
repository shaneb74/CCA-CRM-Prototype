
import streamlit as st
from ui.widgets import inject_css, kpi, section, alert, tile, pill, progress

st.set_page_config(page_title="Advisor Dashboard (Mock)", page_icon="🧭", layout="wide")
inject_css()

# Top: KPIs + alerts
c1,c2,c3,c4 = st.columns(4)
with c1: kpi("New Leads (Today)","5")
with c2: kpi("Assigned Leads","12")
with c3: kpi("Active Cases","3")
with c4: kpi("MTD vs Goal","$20,500 / $40,000","51%")

alert("Don’t forget to upload the signed Disclosure before scheduling tours. Complete intake in CRM.")
alert("Financial reviews should confirm Medicaid rollover. Secure RN assessment 5 days before discharge/tour.")

# Main grid
left, right = st.columns([1.05,1])

# Left: Tasks + Communications
with left:
    section("Tasks & Queues")
    for t in [
        "Call lead John Doe",
        "Follow up with client Jane",
        "Prepare intake forms",
        "Schedule case review",
        "Complete assessment for Mary Johnson"
    ]:
        st.checkbox(t)

    section("Communications")
    st.write("**[Referral]** Harborview MC — *Disclosure still pending*.")
    st.write("**[Family]** Johnson — *Asked about Medicaid timeline*.")
    st.write("**[Community]** Cedar Grove — *Tour confirmation needed*.")
    st.write("**[Clinic]** Northlake Geriatrics — *Needs case summary*.")
    st.caption("These are action-oriented comms. Link out to Outlook/Teams for the full thread.")

    section("Pipeline by Workflow Stage")
    progress("Lead Received", 70)
    progress("Intake", 55)
    progress("Case Management", 25)
    progress("Placement", 40)

# Right: Workflow groups (stages)
with right:
    st.subheader("Advisor Workflows")
    st.markdown("**Lead → Intake**")
    tile("Lead Received","Call client and start intake (~30 min). Upload disclosure before tours.")
    st.markdown("Status "); pill("Due today","due")

    tile("Client Intake","Complete intake in CRM. Keep notes date-stamped with initials.")
    st.markdown("Status "); pill("In progress","due")

    st.write("")
    st.markdown("**Case Management → Search**")
    tile("Case Management","Discuss with CM for barriers, discharge date, log contact.")
    st.markdown("Status "); pill("Needs info","warn")

    tile("AL/MC Search","Submit discovery request via CRM. DFS adds to grid.")
    st.markdown("Status "); pill("Queued","ok")

    st.write("")
    st.markdown("**Decision → Transition → Invoice**")
    tile("Financial Review","Discuss Medicaid rollover, budget. Log in CRM.")
    st.markdown("Status "); pill("Overdue","over")

    tile("Transition to New Home","Schedule move-in within 5 and 30 days post move.")
    st.markdown("Status "); pill("Scheduled","ok")

    tile("Invoice","Send invoice to admin within 3 days. No contract.")
    st.markdown("Status "); pill("Pending","due")

# Bottom strip: upcoming follow-ups
st.write("")
st.subheader("Upcoming Follow-ups")
st.write("Thu — Call with Mary (Harborview DP)")
st.write("Fri — Review RN Assessment (Holt)")
st.write("Mon — Confirm tour time (Cedar Grove)")
