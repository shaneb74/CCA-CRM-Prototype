
import streamlit as st
from data_loader import load_seed
from ui.widgets import inject_css, kpi, section, alert, progress, tile
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
k1,k2,k3,k4 = st.columns(4)
with k1: kpi("New Leads (Today)", "5")
with k2: kpi("Assigned Leads", "12")
with k3: kpi("Active Cases", "2")
with k4: kpi("MTD vs Goal", f"${mtd:,.0f} / ${goal:,.0f}", f"{int(mtd/goal*100)}%")

st.write("")
left, right = st.columns([1.05,1])
with left:
    section("Tasks & Queues")
    for t in ["Call lead John Doe","Follow up with client Jane","Prepare intake forms","Schedule case review","Complete assessment for Mary Johnson"]:
        st.checkbox(t)
    section("Pipeline by Workflow Stage")
    progress("Lead Received", 70); progress("Intake", 55); progress("Case Management", 25); progress("Placement", 40)
with right:
    section("Advisor Workflows")
    g1,g2 = st.columns(2)
    with g1: tile("Lead Received","Call client and start intake (~30 min). Upload disclosure before tours.","pages/11_Client_Record.py","Start Intake Form")
    with g2: tile("Client Intake","Complete intake in CRM. Keep notes date-stamped.","pages/11_Client_Record.py","Open Intake Form")
