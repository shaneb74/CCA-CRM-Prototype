
import streamlit as st
from data_loader import load_seed
from ui.widgets import section, table

st.set_page_config(page_title="Documents", page_icon="📄", layout="wide")
data = load_seed()

section("Template library (mock)")
table([
    {"Template":"State Disclosure","Version":"v2","Type":"e-sign"},
    {"Template":"Tour Guide","Version":"v1","Type":"pdf"},
    {"Template":"Invoice Memo","Version":"v1","Type":"pdf"}
])

st.divider()
section("Recent generated documents")
table(data["documents"])
