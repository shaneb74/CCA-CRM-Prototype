
import streamlit as st
from ui.widgets import inject_css, kpi, section, alert, tile, progress
from data_loader import load_seed

st.set_page_config(page_title="Advisor Dashboard", page_icon="🧭", layout="wide")
inject_css()
data = load_seed()

if "notifications" not in st.session_state:
    st.session_state.notifications = [
        {"id": 1, "type": "Compliance", "pill": "comp", "text": "Upload signed Disclosure before scheduling tours."},
        {"id": 2, "type": "Financial", "pill": "fin", "text": "Confirm Medicaid rollover during financial review."},
        {"id": 3, "type": "General", "pill": "gen", "text": "Keep intake notes date-stamped with initials."}
    ]
if "dismissed" not in st.session_state:
    st.session_state.dismissed = []

# Header KPIs
adv_goal = 40000
mtd = sum(p["fee_amount"] for p in data["placements"])
k1,k2,k3,k4 = st.columns(4)
with k1: kpi("New Leads (Today)","5")
with k2: kpi("Assigned Leads","12")
with k3: kpi("Active Cases","2")
with k4: kpi("MTD vs Goal", f"${mtd:,.0f} / ${adv_goal:,.0f}", f"{int(mtd/adv_goal*100)}%")

st.write("")
# Notifications banners
remaining = [n for n in st.session_state.notifications if n["id"] not in st.session_state.dismissed]
for n in remaining:
    col_text, col_x = st.columns([12,1])
    with col_text: alert(f"{n['text']} <span style='font-size:12px;color:#4c6ef5'>[{n['type']}]</span>")
    with col_x:
        if st.button("✕", key=f"dismiss_{n['id']}"): st.session_state.dismissed.append(n["id"])

left, right = st.columns([1.05,1])
with left:
    with st.expander("Tasks & Queues", expanded=True):
        for t in ["Call lead John Doe","Follow up with client Jane","Prepare intake forms"]:
            st.checkbox(t)
    with st.expander("Communications", expanded=False):
        st.write("**[Referral]** Harborview MC — Disclosure still pending.")
    with st.expander("Pipeline by Workflow Stage", expanded=False):
        progress("Lead Received", 70); progress("Intake", 55); progress("Case Management", 25); progress("Placement", 40)
with right:
    section("Advisor Workflows")
    tile("Lead Received","Call client and start intake. Upload disclosure before tours.")
    tile("Financial Review","Discuss Medicaid rollover, budget. Log in CRM.")
