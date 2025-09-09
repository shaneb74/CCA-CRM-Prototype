
import streamlit as st
from data_loader import load_seed
from ui.widgets import inject_css, kpi

st.set_page_config(page_title="Advisor Workspace", page_icon="💼", layout="wide")
inject_css()
data = load_seed()

adv = data["advisors"][0]
mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"]==adv["id"])
goal = adv["goal_monthly"]
k1,k2,k3,k4 = st.columns(4)
with k1: kpi("New Leads (Today)","5")
with k2: kpi("Assigned Leads","12")
with k3: kpi("Active Cases","3")
with k4: kpi("MTD vs Goal", f"${mtd:,.0f} / ${goal:,.0f}", f"{int(mtd/goal*100)}%")

st.subheader("Pipeline Board")
st.write("Stub pipeline view here")
