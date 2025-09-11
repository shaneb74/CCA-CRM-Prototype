# pages/06_Reporting.py
from __future__ import annotations
import streamlit as st

# --- Safe page-config: do not call st.set_page_config here directly ---
try:
    # Your helper should call st.set_page_config once and early
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    # Fallback guard so we don't double-call in this run
    KEY = "_page_config_applied"
    if not st.session_state.get(KEY):
        try:
            st.set_page_config(page_title="Reporting", page_icon="📊", layout="wide")
        except Exception:
            pass
        st.session_state[KEY] = True

# --- Page UI ---
st.title("Reporting")

st.caption("Pick a sample report to preview the kinds of views we’ll support.")
report = st.selectbox(
    "Choose a report",
    ["Monthly aggregate", "Referral source", "Advisor efficiency"],
    index=0,
    key="reporting_selector",
)

if report == "Monthly aggregate":
    st.subheader("Monthly aggregate (mock)")
    st.write("KPIs by month (leads, assignments, consultations, placements, conversion).")
    st.bar_chart(
        {"Leads": [26, 31, 28, 35], "Consultations": [14, 17, 15, 19], "Placements": [6, 7, 8, 9]}
    )

elif report == "Referral source":
    st.subheader("Referral source (mock)")
    st.write("Breakdown of lead volume and conversion by source.")
    st.bar_chart({"Hospitals": [12], "Attorneys": [8], "Web": [20], "Other": [6]})

else:  # Advisor efficiency
    st.subheader("Advisor efficiency (mock)")
    st.write("Time-to-first-contact, time-to-consultation, and placement rate by advisor.")
    st.dataframe(
        {
            "Advisor": ["Kelsey", "Chanda", "Jenny", "Jennifer"],
            "Time to first contact (hrs)": [1.6, 2.2, 1.1, 2.9],
            "Time to consultation (days)": [1.9, 2.5, 1.7, 2.8],
            "Placement rate": ["28%", "24%", "31%", "26%"],
        }
    )
