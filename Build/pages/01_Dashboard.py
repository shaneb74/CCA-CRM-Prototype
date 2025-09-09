
import streamlit as st
from ui.widgets import inject_css

inject_css()
st.markdown("## Advisor Dashboard")

# At-a-glance section
with st.container():
    st.markdown("<div class='glance-title'>At a glance</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1,1,1,1.3], gap="large")

    with col1:
        st.markdown("<div class='kpi'><span class='kpi-label'>New leads (today)</span><span class='kpi-value'>5</span><span class='pill pill-good'>+2 vs yesterday</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='kpi'><span class='kpi-label'>Assigned leads</span><span class='kpi-value'>12</span><span class='pill pill-good'>+1 this week</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='kpi'><span class='kpi-label'>Active cases</span><span class='kpi-value'>3</span><span class='pill pill-bad'>-1 since Fri</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='kpi'><span class='kpi-label'>MTD vs goal</span><span class='kpi-value'>$20,500 / $40,000</span><span class='pill pill-warn'>51% of goal</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Dismissable blue notices => on dismiss they "move" to Notifications page (simulated via session_state)
st.session_state.setdefault("notice_history", [])
st.session_state.setdefault("notices", [
    {"text":"Upload signed Disclosure before scheduling tours.","type":"Compliance"},
    {"text":"Confirm Medicaid rollover during financial review.","type":"Financial"},
    {"text":"Keep intake notes date-stamped with initials.","type":"General"},
])

def dismiss_notice(i):
    note = st.session_state["notices"].pop(i)
    st.session_state["notice_history"].append(note)

for idx, n in enumerate(list(st.session_state["notices"])):
    cols = st.columns([1, .06])
    with cols[0]:
        st.markdown(f"<div class='note'>{n['text']} <span class='small-muted'>[{n['type']}]</span></div>", unsafe_allow_html=True)
    with cols[1]:
        if st.button("x", key=f"dismiss_{idx}"):
            dismiss_notice(idx)
            st.experimental_rerun()

# Drawers
with st.expander("Tasks & Queues", expanded=True):
    for t in ["Call lead John Doe","Follow up with client Jane","Prepare intake forms","Schedule case review","Complete assessment for Mary Johnson"]:
        st.checkbox(t, value=False)
with st.expander("Communications", expanded=False):
    st.markdown("**[Referral]** Harborview MC — Disclosure still pending.")
with st.expander("Pipeline by Workflow Stage", expanded=False):
    st.progress(0.55, text="Lead → Intake → Case Management → Placement")

# Right column: Advisor Workflows
st.markdown("### Advisor Workflows")
cols = st.columns(1)
with cols[0]:
    with st.expander("Lead → Intake", expanded=True):
        st.write("**Lead Received**")
        st.caption("Call client and start intake (~30 min). Upload disclosure before tours.")
        st.write("**Client Intake**")
        st.caption("Complete intake in CRM. Keep notes date-stamped.")
    with st.expander("Case Management → Search", expanded=False):
        st.write("**Case Management**")
        st.caption("Discuss barriers, discharge date, log contact.")
    with st.expander("Decision → Transition → Invoice", expanded=False):
        st.write("**Financial Review**")
        st.caption("Discuss Medicaid rollover, budget. Log in CRM.")
