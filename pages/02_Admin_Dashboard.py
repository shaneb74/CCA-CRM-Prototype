
import streamlit as st
from ui.widgets import inject_css, kpi, section
from data_loader import load_seed
st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
inject_css()
data = load_seed()
total = sum(p["fee_amount"] for p in data["placements"])
c1,c2,c3 = st.columns(3)
with c1: kpi("Total MTD Fees", f"${total:,.0f}")
with c2: kpi("Total Placements", f"{len(data['placements'])}")
with c3: kpi("Avg Fee", f"${(total/max(1,len(data['placements']))):,.0f}")
section("Rollup table incoming…")
