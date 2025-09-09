
import streamlit as st
from data_loader import load_seed
from ui.widgets import section, table

st.set_page_config(page_title="Prospects", page_icon="📇", layout="wide")
data = load_seed()

section("Prospect list")
table(data["prospects"])

st.divider()
section("Quick add (mock)")
st.text_input("Name/Org")
st.selectbox("Category", ["Discharge Planner","Clinic","Community","Other"])
st.button("Save")
