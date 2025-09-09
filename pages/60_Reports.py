
import streamlit as st
from ui.widgets import inject_css, section
from data_loader import load_seed
st.set_page_config(page_title="Reports", page_icon="📈", layout="wide")
inject_css()
data = load_seed()
section("Goal tracker")
rows=[]
for a in data["advisors"]:
    fees=sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"]==a["id"])
    rows.append({"Advisor":a["name"],"Target":a["goal_monthly"],"MTD":fees,"Attainment %":round(100*fees/max(1,a["goal_monthly"]),1)})
st.dataframe(rows, hide_index=True, use_container_width=True)
section("Placement ledger")
st.dataframe(data["placements"], hide_index=True, use_container_width=True)
