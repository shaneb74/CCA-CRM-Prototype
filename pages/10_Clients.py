
import streamlit as st
from data_loader import load_seed
from ui.widgets import section, table

st.set_page_config(page_title="Clients", page_icon="👥", layout="wide")
data = load_seed()

section("Clients")
table(data["clients"])

st.link_button("Open client record (demo: Margaret Holt)", "11_Client_Record")
