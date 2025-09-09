
import streamlit as st
from ui.widgets import inject_css

inject_css()
st.markdown("## Advisor Workspace")

# Demo data
LEADS = [
    {"id":"holt","name":"Margaret Holt","stage":"Intake","city":"Seattle, WA","next":"Call representative","priority":2,"budget":4500},
    {"id":"cole","name":"Raymond Cole","stage":"Case Mgmt","city":"Tacoma, WA","next":"Request RN assessment","priority":1,"budget":5200},
    {"id":"lane","name":"Grace Lane","stage":"Lead Received","city":"Bellevue, WA","next":"Start intake","priority":3,"budget":3800},
]
st.session_state.setdefault("current_case", LEADS[0]["id"])

def select_case(case_id:str):
    st.session_state["current_case"] = case_id

left, right = st.columns([1,2], gap="large")

with left:
    st.markdown("### Work Queue")
    st.selectbox("Filter", ["My leads","All leads"], index=1, key="wq_filter")
    for lead in LEADS:
        with st.container(border=True):
            st.markdown(f"**{lead['name']} — {lead['stage']}**")
            st.caption(f"{lead['city']} • Next: {lead['next']}")
            if st.button("Open", key=f"open_{lead['id']}"):
                select_case(lead["id"])
                st.experimental_rerun()

with right:
    case = next(x for x in LEADS if x["id"]==st.session_state["current_case"])
    st.markdown("### Case Overview")
    st.markdown(f"**{case['name']}** • {case['city']}")
    st.caption(f"Stage: {case['stage']}   •   Priority: {case['priority']}   •   Budget: ${case['budget']:,}")
    st.text_area("Quick note", placeholder="Add a quick note...")
    st.progress(0.6, text="Intake progress")
    st.selectbox("Care needs", ["Choose options","Medical","Mobility","Cognition"], index=0)
    st.markdown("#### Decision support (last results)")
    st.info("**Recommended:** Assisted Living  \n**Estimated cost:** $8,000 / month")
    st.markdown("")
    if st.button("Open full client record"):
        # Navigate to page 4 (Client Record). Streamlit multipage cannot programmatically navigate,
        # so we display a hint instead.
        st.success("Use the left navigation → **Client Record** to view the full record.")
