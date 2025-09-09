
import streamlit as st
from data_loader import load_seed
from ui.widgets import section, table

st.set_page_config(page_title="Reports", page_icon="📈", layout="wide")
data = load_seed()

section("Goal tracker")
rows = []
for a in data["advisors"]:
    fees = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"]==a["id"])
    rows.append({"Advisor": a["name"], "Target": a["goal_monthly"], "MTD": fees, "Attainment %": round(100*fees/max(1,a["goal_monthly"]),1)})
table(rows)

section("Placement ledger")
table(data["placements"])
