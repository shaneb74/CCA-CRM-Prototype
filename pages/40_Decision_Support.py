
import streamlit as st
from data_loader import load_seed
from ui.widgets import section

st.set_page_config(page_title="Decision Support (mock)", page_icon="🧩", layout="wide")
data = load_seed()

section("Guided Care Plan — last run")
st.success("Recommendation: Assisted Living")
st.write("Flags: moderate dependence, cognitive risk")

section("Cost Planner — last run")
st.info("Monthly care cost: **$4,200**  • Years funded: **6**")

st.caption("Display-only. Replace with outputs from your external tools later.")
