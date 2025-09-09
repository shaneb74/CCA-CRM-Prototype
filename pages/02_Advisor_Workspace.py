# pages/02_Advisor_Workspace.py
import streamlit as st
from data_loader import load_seed
from ui.widgets import inject_css, kpi, chips, tile

st.set_page_config(page_title="Advisor Workspace", page_icon="💼", layout="wide")
inject_css()
data = load_seed()

adv = data["advisors"][0]
mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"] == adv["id"])
goal = adv["goal_monthly"]

# Top KPIs
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi("New leads (today)", "5")
with k2:
    kpi("Assigned leads", "12")
with k3:
    kpi("Active cases", "3")
with k4:
    kpi("MTD vs goal", f"${mtd:,.0f} / ${goal:,.0f}", f"{int(mtd/goal*100)}%")

chips(["Overdue: 2", "Tours this week: 3", "Docs pending: 1"])

# Layout columns
left, center, right = st.columns([1.2, 1.8, 1.1])

# Left: work queue
with left:
    st.markdown("### Work Queue")
    view = st.selectbox("Filter", options=["My leads", "All", "Overdue", "Tours"], index=0)
    for c in data["clients"]:
        st.markdown(
            f"**{c['name']}** — {c['stage']}  \n"
            f"<span class='muted small'>{c['city']} • Next: {c['next']}</span>",
            unsafe_allow_html=True,
        )
        st.divider()

# Center: case details (select first for now)
case = data["clients"][0]
with center:
    st.markdown("### Case Overview")
    st.markdown(f"**{case['name']}** • {case['city']}")
    chips([f"Stage: {case['stage']}", f"Priority: {case['priority']}", f"Budget: ${case['budget']:,.0f}"])
    st.text_area("Quick note", placeholder="Add a quick note...", height=80)

    st.markdown("#### Intake")
    st.progress(40)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.checkbox("Medical", value=True)
    with c2:
        st.checkbox("Mobility", value=False)
    with c3:
        st.checkbox("Cognition", value=False)

    st.markdown("#### Financials")
    st.write("Monthly budget, assets, payer source. MTD goal contribution will calculate post-placement.")

    st.markdown("#### Activities")
    st.write("- Email: Disclosure sent 9/3")
    st.write("- Phone: Spoke with daughter 9/4")
    st.write("- Tour: Cedar Grove 9/7")

# Right: QRG & decision support
with right:
    st.markdown("<div class='ctx-panel'>", unsafe_allow_html=True)

    st.markdown("### QRG Quick Steps")
    qrg_steps = [
        "Lead received → call within 30 minutes.",
        "Start intake; capture rep info and DPOA.",
        "Verify Medicaid rollover during financial review.",
        "Request RN assessment 5 days before discharge/tour.",
        "Upload signed Disclosure before scheduling tours.",
        "Log case notes; date-stamped with initials.",
        "Schedule tours; confirm with SMS/email.",
        "If placed, generate invoice within 3 days.",
    ]
    for s in qrg_steps:
        st.write(f"• {s}")

    st.markdown("### Personas cheat-sheet")
    chips(["Memory care", "Assisted living", "In-home"])
    st.caption("Select persona to view considerations (stub).")

    st.markdown("### Decision Support")
    if st.button("Open Care Plan Recommender (mock)"):
        st.session_state["ds_result"] = {"plan": "In-home care", "notes": "Safety check + part-time caregiver"}
    if st.button("Open Cost Planner (mock)"):
        st.session_state["ds_cost"] = {"estimate": "$4,800/mo", "assumptions": "20 hrs/wk caregiver + supplies"}

    st.markdown("#### Last result")
    plan = st.session_state.get("ds_result", {"plan": "In-home care", "notes": "Safety check + part-time caregiver"})
    cost = st.session_state.get("ds_cost", {"estimate": "$4,800/mo", "assumptions": "20 hrs/wk caregiver + supplies"})
    tile(f"Recommended: {plan['plan']}", plan["notes"])
    tile(f"Estimated Cost: {cost['estimate']}", cost["assumptions"])

    st.markdown("</div>", unsafe_allow_html=True)