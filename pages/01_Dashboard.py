
import streamlit as st
from ui.widgets import inject_css, section, tile, progress, at_a_glance, kpi_block
from data_loader import load_seed

st.set_page_config(page_title="Advisor Dashboard", page_icon="🧭", layout="wide")
inject_css()
data = load_seed()

if "notifications" not in st.session_state:
    st.session_state.notifications = [
        {"id": 1, "type": "Compliance", "text": "Upload signed Disclosure before scheduling tours."},
        {"id": 2, "type": "Financial", "text": "Confirm Medicaid rollover during financial review."},
        {"id": 3, "type": "General", "text": "Keep intake notes date-stamped with initials."}
    ]
if "dismissed" not in st.session_state:
    st.session_state.dismissed = []

adv = data["advisors"][0]
mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"] == adv["id"])
goal = adv["goal_monthly"]
pct = 0 if goal == 0 else int((mtd/goal)*100)

def render_kpis(c1, c2, c3, c4):
    kpi_block(c1, "New leads (today)", "5", delta="+2 vs yesterday", intent="pos")
    kpi_block(c2, "Assigned leads", "12", delta="+1 this week", intent="pos")
    kpi_block(c3, "Active cases", str(len(data["clients"])), delta="−1 since Fri", intent="neg")
    kpi_block(c4, "MTD vs goal", f"${mtd:,.0f} / ${goal:,.0f}", subtitle=f"{pct}% achieved", delta=f"{pct}% of goal", intent="neu")

at_a_glance(render_kpis, pills=["This week: 2 placements", "Pending: $15,500", "Tours booked: 3"])

remaining = [n for n in st.session_state.notifications if n["id"] not in st.session_state.dismissed]
for n in remaining:
    col_text, col_x = st.columns([12,1])
    with col_text:
        st.info(n["text"])
    with col_x:
        if st.button("✕", key=f"dismiss_{n['id']}"): st.session_state.dismissed.append(n["id"])

left, right = st.columns([1.05,1])
with left:
    with st.expander("Tasks & Queues", expanded=True):
        for t in ["Call lead John Doe","Follow up with client Jane","Prepare intake forms","Schedule case review","Complete assessment for Mary Johnson"]:
            st.checkbox(t)
    with st.expander("Communications", expanded=False):
        st.write("**[Referral]** Harborview MC — Disclosure still pending.")
        st.write("**[Family]** Johnson — Asked about Medicaid timeline.")
        st.write("**[Community]** Cedar Grove — Tour confirmation needed.")
        st.caption("Action-oriented comms. Outlook/Teams integration later.")
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
