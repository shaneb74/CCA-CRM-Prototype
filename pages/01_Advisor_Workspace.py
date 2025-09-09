
import streamlit as st
from data_loader import load_seed
from ui.widgets import inject_css, kpi, banner, card, tag

st.set_page_config(page_title="Advisor Workspace", page_icon="🧭", layout="wide")
inject_css()
data = load_seed()

if "dismissed" not in st.session_state: st.session_state.dismissed = []
if "selected_client" not in st.session_state: st.session_state.selected_client = None

adv = data["advisors"][0]
mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"]==adv["id"])
goal = adv["goal_monthly"]
unread = [n for n in data["notifications"] if n["id"] not in st.session_state.dismissed]

st.markdown("<div class='sticky'>", unsafe_allow_html=True)
h1,h2,h3,h4,h5 = st.columns([2,1,1,1,1])
with h1:
    st.text_input("Global search", placeholder="Search clients, communities, prospects…", label_visibility="collapsed")
with h2: kpi("New Leads (Today)","5")
with h3: kpi("Assigned Leads","12")
with h4: kpi("Active Cases","3")
with h5:
    kpi("MTD vs Goal", f"${mtd:,.0f} / ${goal:,.0f}", f"{int(mtd/goal*100)}%")
    st.page_link("pages/03_Notifications.py", label=f"🔔 Notifications ({len(unread)})")
st.markdown("</div>", unsafe_allow_html=True)

t1,t2,t3 = st.columns(3)
with t1: card("Today","2 tasks due • 1 overdue")
with t2: card("Comms","1 unread family email • 1 community follow-up")
with t3: card("Appointments","RN assessment request pending")

for n in unread:
    cols = st.columns([12,1])
    with cols[0]:
        banner(f"{n['text']} <span class='pill {n['pill']}'>" + n["type"] + "</span>")
    with cols[1]:
        if st.button("✕", key=f"x_{n['id']}", help="Mark handled and archive to Notifications"):
            st.session_state.dismissed.append(n["id"])

left, right = st.columns([1.6,1])
with left:
    with st.expander("Action Queue (prioritized)", expanded=True):
        items = sorted(data["tasks"], key=lambda x: -x["importance"])
        for item in items:
            st.checkbox(f"{item['text']}  ·  {item['due']}", key=f"chk_{item['id']}")
    st.write("")
    st.subheader("Pipeline Board")
    cols = st.columns(4)
    col_map = dict(zip(data["stages"], cols))
    for stage in data["stages"]:
        with col_map[stage]:
            st.markdown(f"**{stage}**")
            stage_clients = [c for c in data["clients"] if c["stage"]==stage]
            if not stage_clients:
                st.caption("No items")
            for c in stage_clients:
                if st.button(f"{c['name']} · {c['city']}", key=f"sel_{c['id']}"):
                    st.session_state.selected_client = c['id']
                st.caption(f"Next: {c['next']}")
                if c["tags"]:
                    st.caption("Tags: " + ", ".join(c["tags"]))
                st.divider()

with right:
    st.subheader("Context")
    cid = st.session_state.selected_client
    if cid:
        c = next((x for x in data["clients"] if x["id"]==cid), None)
        if c:
            st.markdown(f"**{c['name']}** — {c['city']}")
            st.caption(f"Stage: {c['stage']}  ·  Budget: ${c['budget']:,.0f}")
            st.write("")
            st.markdown("**Quick actions**"); st.button("Open Intake"); st.button("Start Financial Review"); st.button("Schedule Tour"); st.button("Create Invoice")
            st.write("")
            st.markdown("**Recent activity**"); st.write("- Called representative; left voicemail"); st.write("- Received self-service intake")
            st.write("")
            st.markdown("**Docs**"); st.write("- State Disclosure — Signed"); st.write("- RN Assessment — Pending")
    else:
        st.caption("Select a client card from the Pipeline Board to open details here.")
