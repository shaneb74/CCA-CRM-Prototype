
import streamlit as st
from ui.widgets import inject_css, card, chips, tile

inject_css()
st.title("Client Record")

with card("Header"):
    st.markdown("**Grace Lane** — Bellevue, WA")
    chips(["Stage: Intake","DPOA on file","Allergies: None"])

col1, col2 = st.columns(2, gap="large")
with col1:
    with card("Medical"):
        st.text_input("Primary diagnosis", value="MCI")
        st.text_input("Mobility", value="Walker")
        st.text_input("Cognition", value="Moderate")
    with card("Contacts"):
        st.text_input("Representative name", value="Mary Lane")
        st.text_input("Phone", value="(206) 555-1212")
with col2:
    with card("Financials"):
        st.number_input("Monthly budget", value=8000, step=100)
        st.text_input("Payer source", value="Private pay")
    with card("Activities"):
        st.write("• Email: Disclosure sent 9/3")
        st.write("• Phone: Spoke with daughter 9/4")
        st.write("• Tour: Cedar Grove 9/7")
