
import streamlit as st
from ui.widgets import section, table
from data_loader import load_seed

st.set_page_config(page_title="Clients", page_icon="👥", layout="wide")
data = load_seed()
section("Clients")
table(data["clients"])
