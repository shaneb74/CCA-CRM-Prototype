# pages/06_Reporting.py
from __future__ import annotations
import streamlit as st

# Safe page-config & redirect wrapper (no-op if already set)
try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    # Fallback guard: only set config if not already set this run
    if "_page_config_applied" not in st.session_state:
        try:
            st.set_page_config(page_title="Reporting", page_icon="📊", layout="wide")
        except Exception:
            pass
        st.session_state["_page_config_applied"] = True

st.set_page_config(page_title="Reporting", page_icon="📊", layout="wide")

st.title("Reporting")

report = st.selectbox(
    "Select a report",
    ["Monthly Aggregate", "Referral Sources", "Advisor Efficiency"],
    index=0,
    key="reporting_select",
)

st.divider()

if report == "Monthly Aggregate":
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("New leads (month)", 126, "+8%")
    with c2: st.metric("Qualified", "62", "+3")
    with c3: st.metric("Placements", "31", "+2")
    with c4: st.metric("Conversion rate", "24.6%", "+0.7pp")

    st.subheader("By week")
    st.dataframe({
        "Week": ["W1", "W2", "W3", "W4"],
        "Leads": [28, 31, 34, 33],
        "Qualified": [13, 16, 18, 15],
        "Placements": [6, 7, 9, 9],
    }, use_container_width=True)

elif report == "Referral Sources":
    st.caption("Top referral sources this month (mock)")
    st.dataframe({
        "Source": ["Hospital A", "Hospital B", "Home Health C", "Website", "Friend/Family"],
        "Leads": [22, 17, 14, 38, 35],
        "Qualified": [14, 10, 8, 18, 12],
        "Placements": [7, 5, 4, 9, 6],
    }, use_container_width=True)

elif report == "Advisor Efficiency":
    st.caption("Time-to-first-contact and placement conversion by advisor (mock)")
    st.dataframe({
        "Advisor": ["Kelsey Jochum", "Jennifer James", "Jenny Krzemien", "Chanda Hickman"],
        "Avg. time to 1st contact": ["1.4h", "2.1h", "1.8h", "2.7h"],
        "Leads this month": [32, 27, 29, 24],
        "Placements": [12, 10, 9, 7],
        "Conversion": ["37.5%", "37.0%", "31.0%", "29.2%"],
    }, use_container_width=True)
