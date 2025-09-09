
import streamlit as st
from ui.widgets import inject_css, section
from data_loader import load_seed
st.set_page_config(page_title="Clients", page_icon="👥", layout="wide")
inject_css()
data = load_seed()
section("Clients")
st.dataframe(data["clients"], hide_index=True, use_container_width=True)
st.link_button("Open client record (demo: Margaret Holt)", "11_Client_Record")
