
import streamlit as st
from ui.widgets import inject_css, section
st.set_page_config(page_title="Decision Support (mock)", page_icon="🧩", layout="wide")
inject_css()
section("Guided Care Plan — last run"); st.success("Recommendation: Assisted Living"); st.write("Flags: moderate dependence, cognitive risk")
section("Cost Planner — last run"); st.info("Monthly care cost: **$4,200**  • Years funded: **6**")
st.caption("Display-only. Replace with outputs from your external tools later.")
