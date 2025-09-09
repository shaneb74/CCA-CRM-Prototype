
import streamlit as st
from ui.widgets import inject_css

inject_css()
st.markdown("## Client Record")

st.text_input("Banner", placeholder="(Optional internal banner message)")

st.markdown("### Header")
st.write("Grace Lane — Bellevue, WA")
st.caption("Stage: Intake   •   DPOA on file   •   Allergies: None")
st.text_input("Primary contact", value="")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Medical")
    st.text_input("Primary diagnosis", value="MCI")
    st.text_input("Mobility", value="Walker")
    st.text_input("Cognition", value="Moderate")
with col2:
    st.markdown("### Financials")
    st.number_input("Monthly budget", value=8000, step=100)
    st.text_input("Payer source", value="Private pay")

st.markdown("### Activities")
st.write("• Email: Disclosure sent 9/3")
st.write("• Phone: Spoke with daughter 9/4")
st.write("• Tour: Cedar Grove 9/7")
