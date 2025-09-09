
import streamlit as st
from ui.widgets import inject_css, kpi, alert, tile, progress, section
from data_loader import load_seed

st.set_page_config(page_title="Advisor Dashboard Mock", page_icon="🧭", layout="wide")
inject_css()
data = load_seed()

if "dismissed" not in st.session_state: st.session_state.dismissed = []

adv = data["advisors"][0]; goal = adv["goal_monthly"]
mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"]==adv["id"])
unread = [n for n in data["notifications"] if n['id'] not in st.session_state.dismissed]

with st.container():
    st.markdown("<div class='sticky'>", unsafe_allow_html=True)
    k1,k2,k3,k4 = st.columns(4)
    with k1: kpi("New Leads (Today)","5")
    with k2: kpi("Assigned Leads","12")
    with k3: kpi("Active Cases","2")
    with k4: kpi("MTD vs Goal", f"${mtd:,.0f} / ${goal:,.0f}", f"{int(mtd/goal*100)}%")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
for n in unread:
    c1,c2 = st.columns([12,1])
    with c1: alert(f"{n['text']} <span style='font-size:12px;color:#4c6ef5'>[{n['type']}]</span>")
    with c2:
        if st.button("✕", key=f"dx_{n['id']}"): st.session_state.dismissed.append(n['id'])

left, right = st.columns([1.05,1])
with left:
    with st.expander("Tasks & Queues", expanded=True):
        for t in ["Call lead John Doe","Follow up with client Jane","Prepare intake forms","Schedule case review","Complete assessment for Mary Johnson"]:
            st.checkbox(t)
    with st.expander("Communications", expanded=False):
        st.write("**[Referral]** Harborview MC — Disclosure still pending.")
        st.write("**[Family]** Johnson — Asked about Medicaid timeline.")
        st.write("**[Community]** Cedar Grove — Tour confirmation needed.")
        st.write("**[Clinic]** Northlake Geriatrics — Needs case summary.")
        st.caption("Action-oriented comms. Link to Outlook/Teams later.")
    with st.expander("Pipeline by Workflow Stage", expanded=False):
        progress("Lead Received", 70); progress("Intake", 55); progress("Case Management", 25); progress("Placement", 40)

with right:
    section("Advisor Workflows")
    st.markdown("**Lead → Intake**")
    tile("Lead Received","Call client and start intake (~30 min). Upload disclosure before tours.")
    tile("Client Intake","Complete intake in CRM. Keep notes date-stamped.")
    st.markdown("**Case Management → Search**")
    tile("Case Management","Discuss barriers, discharge date, log contact.")
    tile("AL/MC Search","Submit discovery request via CRM. DFS adds to grid.")
    st.markdown("**Decision → Transition → Invoice**")
    tile("Financial Review","Discuss Medicaid rollover, budget. Log in CRM.")
    tile("Transition to New Home","Schedule move-in within 5 and 30 days post move.")
    tile("Invoice","Send invoice to admin within 3 days. No contract.")
