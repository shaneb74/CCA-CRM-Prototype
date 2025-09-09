
import streamlit as st
from data_loader import load_seed
from ui.widgets import inject_css, kpi, section, alert, tile, progress

st.set_page_config(page_title="Advisor Dashboard", page_icon="🧭", layout="wide")
inject_css()
data = load_seed()

c1,c2,c3,c4 = st.columns([3,1,1,1])
with c1: st.markdown("### CCA  Advisor Dashboard")
with c2: st.page_link("pages/11_Client_Record.py", label="Start Intake")
with c3: st.page_link("pages/40_Decision_Support.py", label="Cost Planner")
with c4: st.page_link("pages/10_Clients.py", label="Next Lead")

alert("Don’t forget to upload the signed Disclosure before scheduling tours. Complete intake in CRM. Keep notes date-stamped with initials.")
alert("Financial reviews should confirm Medicaid rollover. Secure RN assessment 5 days before discharge/tour.")

adv = data["advisors"][0]; adv_id = adv["id"]; goal = adv["goal_monthly"]
mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"]==adv_id)
assigned = 12; new_leads = 5; active = len([c for c in data["clients"] if c["advisor_id"]==adv_id])

k1,k2,k3,k4 = st.columns(4)
with k1: kpi("New Leads (Today)", str(new_leads))
with k2: kpi("Assigned Leads", str(assigned))
with k3: kpi("Active Cases", str(active))
with k4: kpi("MTD vs Goal", f"${mtd:,.0f} / ${goal:,.0f}", f"{int(mtd/goal*100)}%")

st.write("")
left, right = st.columns([1.05,1])

with left:
    section("Tasks & Queues")
    st.checkbox("Call lead John Doe")
    st.checkbox("Follow up with client Jane")
    st.checkbox("Prepare intake forms")
    st.checkbox("Schedule case review")
    st.checkbox("Complete assessment for Mary Johnson")
    section("Pipeline by Workflow Stage")
    progress("Lead Received", 70); progress("Intake", 55); progress("Case Management", 25); progress("Placement", 40)
    section("Information Hub")
    st.write("• Update on compliance changes")
    st.write("• Checklist optimization guide")
    st.write("• Policy note")
    st.page_link("pages/50_Documents.py", label="Care plan documentation »")

with right:
    section("Advisor Workflows")
    g1,g2 = st.columns(2)
    with g1: tile("Lead Received", "Call client and start intake (~30 min). Upload disclosure doc before tours.", link="pages/11_Client_Record.py", link_label="Start Intake Form")
    with g2: tile("Client Intake", "Complete intake in CRM. Keep notes date-stamped with initials.", link="pages/11_Client_Record.py", link_label="Open Intake Form")
    g3,g4 = st.columns(2)
    with g3: tile("Case Management", "Discuss with CM for barriers, discharge date, log contact.", link="pages/60_Reports.py", link_label="Start Financial Review")
    with g4: tile("Financial Review", "Discuss Medicaid rollover, budget. Log in CRM.", link="pages/60_Reports.py", link_label="Start Financial Review")
    g5,g6 = st.columns(2)
    with g5: tile("Adult Family Home Search", "Secure RN assessment 5 days before tour. Request DFS verification.", link="pages/20_Communities.py", link_label="Schedule RN Assessment")
    with g6: tile("AL/MC Search", "Submit discovery request via CRM. DFS adds to grid.", link="pages/20_Communities.py", link_label="Submit Discovery")
    g7,g8 = st.columns(2)
    with g7: tile("Transition to New Home", "Schedule move-in within 5 and 30 days post move.", link="pages/10_Clients.py", link_label="Schedule Move-in")
    with g8: tile("Invoice", "Send invoice to admin within 3 days. No contract.", link="pages/50_Documents.py", link_label="Create Invoice")
