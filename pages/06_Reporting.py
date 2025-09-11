# pages/06_Reporting.py
# Simple, table-first Reporting page (matches dev look)

from __future__ import annotations
import streamlit as st

# --- page chrome (safe: won't double-call set_page_config) ---
try:
    from ui_chrome import apply_chrome  # your helper that safely sets wide + any CSS
    apply_chrome()
except Exception:
    # Fallback: only set once, as early as possible
    try:
        st.set_page_config(page_title="Reporting", page_icon="📊", layout="wide")
    except Exception:
        pass

st.title("Reporting")

st.caption("Pick a sample report to preview the kinds of views we’ll support.")

# --- selector ---
options = ["Referral Sources", "Monthly aggregate", "Agent efficiency"]
report = st.selectbox("Choose a report", options=options, index=0, key="report_selector")

st.write("")  # breathing room

# ---- Helpers to render simple tables to match your dev look ----
def _table_referral_sources():
    st.subheader("Top referral sources this month (mock)")
    data = [
        {"Source": "Hospital A",  "Leads": 22, "Qualified": 14, "Placements": 7},
        {"Source": "Hospital B",  "Leads": 17, "Qualified": 10, "Placements": 5},
        {"Source": "Home Health C","Leads": 14, "Qualified":  8, "Placements": 4},
        {"Source": "Website",     "Leads": 38, "Qualified": 18, "Placements": 9},
        {"Source": "Friend/Family","Leads": 35, "Qualified": 12, "Placements": 6},
    ]
    st.table(data)

def _table_monthly_aggregate():
    st.subheader("Monthly aggregate (mock)")
    st.caption("KPI rollups by month: leads, assignments, consultations, placements, conversion.")
    data = [
        {"Month": "Jan", "Leads": 48, "Assigned": 46, "Consultations": 31, "Placements": 12, "Conversion %": "25%"},
        {"Month": "Feb", "Leads": 56, "Assigned": 53, "Consultations": 35, "Placements": 14, "Conversion %": "25%"},
        {"Month": "Mar", "Leads": 50, "Assigned": 48, "Consultations": 33, "Placements": 11, "Conversion %": "22%"},
        {"Month": "Apr", "Leads": 62, "Assigned": 59, "Consultations": 41, "Placements": 17, "Conversion %": "28%"},
    ]
    st.table(data)

def _table_agent_efficiency():
    st.subheader("Agent efficiency (mock)")
    st.caption("Per-advisor volume and cycle-time snapshots.")
    data = [
        {"Advisor": "Kelsey Jochum",   "Leads": 26, "Consultations": 19, "Placements": 9,  "Avg days to qualify": 4},
        {"Advisor": "Jenny Krzemien",  "Leads": 24, "Consultations": 17, "Placements": 8,  "Avg days to qualify": 5},
        {"Advisor": "Jennifer White",  "Leads": 21, "Consultations": 15, "Placements": 7,  "Avg days to qualify": 5},
        {"Advisor": "Jennifer James",  "Leads": 18, "Consultations": 12, "Placements": 5,  "Avg days to qualify": 6},
        {"Advisor": "Jesiah Irish",    "Leads": 20, "Consultations": 14, "Placements": 6,  "Avg days to qualify": 6},
    ]
    st.table(data)

# --- render selected ---
if report == "Referral Sources":
    _table_referral_sources()
elif report == "Monthly aggregate":
    _table_monthly_aggregate()
else:
    _table_agent_efficiency()
