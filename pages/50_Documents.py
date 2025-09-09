
import streamlit as st
from ui.widgets import inject_css, section
from data_loader import load_seed
st.set_page_config(page_title="Documents", page_icon="📄", layout="wide")
inject_css()
data = load_seed()
section("Template library (mock)")
st.dataframe([{"Template":"State Disclosure","Version":"v2","Type":"e-sign"},
              {"Template":"Tour Guide","Version":"v1","Type":"pdf"},
              {"Template":"Invoice Memo","Version":"v1","Type":"pdf"}], hide_index=True, use_container_width=True)
section("Recent generated documents")
st.dataframe(data["documents"], hide_index=True, use_container_width=True)
