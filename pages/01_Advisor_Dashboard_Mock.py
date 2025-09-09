
import streamlit as st
from ui.widgets import inject_css, kpi, section, alert, tile
from data_loader import load_seed

st.set_page_config(page_title="Advisor Dashboard (Notifications Mock)", page_icon="🧭", layout="wide")
inject_css()
data = load_seed()

# Session state for notifications
if "notifications" not in st.session_state:
    st.session_state.notifications = [
        {"id": 1, "type": "Compliance", "pill": "comp", "text": "Upload signed Disclosure before scheduling tours."},
        {"id": 2, "type": "Financial", "pill": "fin", "text": "Confirm Medicaid rollover during financial review."},
        {"id": 3, "type": "General", "pill": "gen", "text": "Keep intake notes date-stamped with initials."}
    ]
if "dismissed" not in st.session_state:
    st.session_state.dismissed = []
if "show_drawer" not in st.session_state:
    st.session_state.show_drawer = False
if "filter_types" not in st.session_state:
    st.session_state.filter_types = {"Compliance": True, "Financial": True, "General": True}

# Header actions
top_l, top_r = st.columns([1,1])
with top_l:
    st.caption("")
with top_r:
    if st.button("🔔 Notifications"):
        st.session_state.show_drawer = True

# Sticky KPI bar
with st.container():
    st.markdown("<div class='sticky'>", unsafe_allow_html=True)
    k1,k2,k3,k4 = st.columns(4)
    adv = data["advisors"][0]; adv_id = adv["id"]; goal = adv["goal_monthly"]
    mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"]==adv_id)
    with k1: kpi("New Leads (Today)","5")
    with k2: kpi("Assigned Leads","12")
    with k3: kpi("Active Cases","2")
    with k4: kpi("MTD vs Goal", f"${mtd:,.0f} / ${goal:,.0f}", f"{int(mtd/goal*100)}%")
    st.markdown("</div>", unsafe_allow_html=True)

# Inline banners (dismiss to drawer)
st.write("")
remaining = [n for n in st.session_state.notifications if n["id"] not in st.session_state.dismissed]
if remaining:
    b1,b2 = st.columns([3,1])
    with b1:
        for n in remaining:
            alert(f"{n['text']} <span style='font-size:12px;color:#4c6ef5'>[{n['type']}]</span>")
    with b2:
        for n in remaining:
            if st.button(f"Mark handled #{n['id']}", key=f"handle_{n['id']}"):
                st.session_state.dismissed.append(n["id"])

# Two-column layout with collapsibles
left, right = st.columns([1.05,1])

with left:
    with st.expander("Tasks & Queues", expanded=True):
        for t in [
            "Call lead John Doe",
            "Follow up with client Jane",
            "Prepare intake forms",
            "Schedule case review",
            "Complete assessment for Mary Johnson"
        ]:
            st.checkbox(t)
    with st.expander("Communications", expanded=False):
        st.write("**[Referral]** Harborview MC — Disclosure still pending.")
        st.write("**[Family]** Johnson — Asked about Medicaid timeline.")
        st.write("**[Community]** Cedar Grove — Tour confirmation needed.")
        st.write("**[Clinic]** Northlake Geriatrics — Needs case summary.")
        st.caption("Action-oriented comms. Link to Outlook/Teams later.")
    with st.expander("Pipeline by Workflow Stage", expanded=False):
        st.progress(70, text="Lead Received")
        st.progress(55, text="Intake")
        st.progress(25, text="Case Management")
        st.progress(40, text="Placement")

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

st.write("")
st.subheader("Upcoming Follow-ups")
st.write("Thu — Call with Mary (Harborview DP)")
st.write("Fri — Review RN Assessment (Holt)")
st.write("Mon — Confirm tour time (Cedar Grove)")

# Drawer UI (right overlay)
if st.session_state.show_drawer:
    # Render overlay drawer via HTML/JS-free approach using absolute positioned div
    st.markdown("<div class='drawer'>", unsafe_allow_html=True)
    st.markdown("### Notifications")
    # Filters
    colf1, colf2, colf3 = st.columns(3)
    with colf1:
        st.session_state.filter_types["Compliance"] = st.checkbox("Compliance", value=st.session_state.filter_types["Compliance"])
    with colf2:
        st.session_state.filter_types["Financial"] = st.checkbox("Financial", value=st.session_state.filter_types["Financial"])
    with colf3:
        st.session_state.filter_types["General"] = st.checkbox("General", value=st.session_state.filter_types["General"])

    # List dismissed and active
    st.markdown("#### Unread")
    for n in remaining:
        if st.session_state.filter_types.get(n["type"], True):
            st.write(f"- {n['text']}  
  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)

    st.markdown("#### History")
    for n in [x for x in st.session_state.notifications if x['id'] in st.session_state.dismissed]:
        if st.session_state.filter_types.get(n["type"], True):
            st.write(f"- {n['text']}  
  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)

    if st.button("Close"):
        st.session_state.show_drawer = False
    st.markdown("</div>", unsafe_allow_html=True)
