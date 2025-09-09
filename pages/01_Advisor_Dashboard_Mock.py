
import streamlit as st
from ui.widgets import inject_css, kpi, section, alert, tile, progress
from data_loader import load_seed

st.set_page_config(page_title="Advisor Dashboard (Notifications Mock)", page_icon="🧭", layout="wide")
inject_css()
data = load_seed()

# Session state
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

# Header
hdr_left, hdr_right = st.columns([1,1])
with hdr_left: st.caption("")
with hdr_right:
    if st.button("🔔 Notifications", help="Open notifications panel"):
        st.session_state.show_drawer = True

# Sticky KPI row
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

st.write("")

# Inline banners with ✕ control (moves to notifications history)
remaining = [n for n in st.session_state.notifications if n["id"] not in st.session_state.dismissed]
for n in remaining:
    col_text, col_x = st.columns([12,1])
    with col_text:
        alert(f"{n['text']} <span style='font-size:12px;color:#4c6ef5'>[{n['type']}]</span>")
    with col_x:
        if st.button("✕", key=f"dismiss_{n['id']}", help="Mark handled and move to Notifications"):
            st.session_state.dismissed.append(n["id"])

# Main content with collapsibles + optional drawer column
if st.session_state.show_drawer:
    main_col, drawer_col = st.columns([3,1.1])
else:
    main_col = st.container()

with main_col:
    left, right = st.columns([1.05,1])
    with left:
        with st.expander("Tasks & Queues", expanded=True):
            for t in [
                "Call lead John Doe",
                "Follow up with client Jane",
                "Prepare intake forms",
                "Schedule case review",
                "Complete assessment for Mary Johnson"]:
                st.checkbox(t)
        with st.expander("Communications", expanded=False):
            st.write("**[Referral]** Harborview MC — Disclosure still pending.")
            st.write("**[Family]** Johnson — Asked about Medicaid timeline.")
            st.write("**[Community]** Cedar Grove — Tour confirmation needed.")
            st.write("**[Clinic]** Northlake Geriatrics — Needs case summary.")
            st.caption("Action-oriented comms. Link to Outlook/Teams later.")
        with st.expander("Pipeline by Workflow Stage", expanded=False):
            progress("Lead Received", 70)
            progress("Intake", 55)
            progress("Case Management", 25)
            progress("Placement", 40)
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

# Drawer column content (native widgets, so it opens/closes correctly)
if st.session_state.show_drawer:
    with drawer_col:
        st.markdown("### Notifications")
        # Filters
        st.write("Filters")
        f1,f2,f3 = st.columns(3)
        with f1:
            st.session_state.filter_types["Compliance"] = st.checkbox("Compliance", value=st.session_state.filter_types["Compliance"])
        with f2:
            st.session_state.filter_types["Financial"] = st.checkbox("Financial", value=st.session_state.filter_types["Financial"])
        with f3:
            st.session_state.filter_types["General"] = st.checkbox("General", value=st.session_state.filter_types["General"])

        # Unread
        st.markdown("#### Unread")
        unread = [n for n in st.session_state.notifications if n["id"] not in st.session_state.dismissed]
        any_unread = False
        for n in unread:
            if st.session_state.filter_types.get(n["type"], True):
                any_unread = True
                st.markdown(f"- {n['text']}  \n  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)
        if not any_unread:
            st.caption("No unread.")

        # History
        st.markdown("#### History")
        hist = [n for n in st.session_state.notifications if n["id"] in st.session_state.dismissed]
        any_hist = False
        for n in hist:
            if st.session_state.filter_types.get(n["type"], True):
                any_hist = True
                st.markdown(f"- {n['text']}  \n  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)
        if not any_hist:
            st.caption("No history yet.")

        if st.button("Close"):
            st.session_state.show_drawer = False
