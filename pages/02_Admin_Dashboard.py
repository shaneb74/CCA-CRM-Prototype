
import streamlit as st
from data_loader import load_seed
from ui.widgets import kpi, table, section

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
data = load_seed()

# Revenue by advisor
rev = {}
for p in data["placements"]:
    rev[p["advisor_id"]] = rev.get(p["advisor_id"], 0) + p["fee_amount"]
adv_map = {a["id"]: a["name"] for a in data["advisors"]}
rows = [{"Advisor": adv_map.get(k, k), "MTD Fees": v} for k,v in rev.items()]

c1,c2,c3 = st.columns(3)
with c1: kpi("Total MTD Fees", f"${sum(r['MTD Fees'] for r in rows):,.0f}")
with c2: kpi("Total Placements", f"{len(data['placements'])}")
with c3: kpi("Avg Fee", f"${(sum(r['MTD Fees'] for r in rows)/max(1,len(data['placements']))):,.0f}")

st.divider()
section("Revenue by advisor")
table(rows)

st.divider()
section("Compliance tiles (mock)")
st.write("- Disclosures signed before tours: 92%")
st.write("- Invoices sent within 3 days: 88%")
st.write("- Required docs by stage: 94%")
