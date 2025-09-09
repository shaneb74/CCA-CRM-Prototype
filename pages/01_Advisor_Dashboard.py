
import streamlit as st
from data_loader import load_seed
from ui.widgets import section, table, kpi

st.set_page_config(page_title="Advisor Dashboard", page_icon="🧭", layout="wide")
data = load_seed()

adv_names = [a["name"] for a in data["advisors"]]
adv = st.selectbox("Advisor", adv_names, index=0)
goal = next(a["goal_monthly"] for a in data["advisors"] if a["name"]==adv)
adv_id = next(a["id"] for a in data["advisors"] if a["name"]==adv)
mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"]==adv_id)

c1,c2,c3,c4 = st.columns(4)
with c1: kpi("Target", f"${goal:,.0f}")
with c2: kpi("MTD fees", f"${mtd:,.0f}")
with c3: kpi("Attainment", f"{(mtd/goal*100):.0f}%")
with c4: kpi("Placements", f"{sum(1 for p in data['placements'] if p['advisor_id']==adv_id)}")

st.divider()
section("Active clients")
rows = [c for c in data["clients"] if c["advisor_id"]==adv_id]
table(rows)

st.divider()
section("Recent DS runs")
client_name = {c["id"]: c["name"] for c in data["clients"]}
ds = [{**r, "client": client_name.get(r["client_id"], "")} for r in data["ds_runs"]]
table(ds)
