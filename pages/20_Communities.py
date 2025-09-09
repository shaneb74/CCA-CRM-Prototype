
import streamlit as st
from data_loader import load_seed
from ui.widgets import section, table

st.set_page_config(page_title="Communities", page_icon="🏠", layout="wide")
data = load_seed()

section("Directory")
q = st.text_input("Search by name, city, capability")
items = data["communities"]
if q:
    ql = q.lower()
    items = [c for c in items if ql in c["name"].lower() or ql in c["city"].lower() or any(ql in cap for cap in c["capabilities"])]
table(items)

st.divider()
section("Filters (facets) — demo only")
st.multiselect("Capabilities", ["dementia","hoyer","awake nights","secured","wander guard","wheelchair"])
st.selectbox("Medicaid window", ["Any","None","6 months","12 months"])
