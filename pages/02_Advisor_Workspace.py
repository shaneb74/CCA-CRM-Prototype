
import streamlit as st
from ui.widgets import inject_css, card, chips, tile

inject_css()
st.title("Advisor Workspace")

left, right = st.columns([1,2], gap="large")

with left:
    st.subheader("Work Queue")
    st.selectbox("Filter", ["My leads","All leads"], index=0)
    for name, stage, next_step in [
        ("Margaret Holt", "Intake", "Call representative"),
        ("Raymond Cole", "Case Mgmt", "Request RN assessment"),
        ("Grace Lane", "Lead Received", "Start intake"),
    ]:
        with card(None):
            st.markdown(f"**{name} — {stage}**")
            st.caption(f"Next: {next_step}")
            st.button("Open", key=f"open_{name.replace(' ','_')}")

with right:
    st.subheader("Case Overview")
    st.markdown("**Grace Lane • Bellevue, WA**")
    chips(["Stage: Lead Received","Priority: 3","Budget: $3,800"])
    st.text_area("Quick note", placeholder="Add a quick note...")

    with card("Intake"):
        st.progress(0.4)

    with card("Care needs"):
        st.multiselect("Choose options", ["Medical","Mobility","Cognition"], default=[])

    with card("Financials"):
        st.caption("Monthly budget, assets, payer source. MTD goal contribution will calculate post-placement.")

    with card("Decision support (last results)"):
        st.write("**Recommended:** Assisted living")
        st.write("**Estimated cost:** $8,000 / month")

    st.button("Open full client record", key="open_full_record")
