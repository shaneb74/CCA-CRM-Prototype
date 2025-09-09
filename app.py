
import streamlit as st
from ui.widgets import inject_css

import streamlit as st

st.set_page_config(
    page_title="Advisor Dashboard",
    layout="wide",   # <-- this is the magic word
    initial_sidebar_state="expanded"
)

st.set_page_config(page_title="Senior CRM Prototype", page_icon="📋", layout="wide")
inject_css()

st.markdown("# app")
st.markdown("This is the landing page for initialization.  Click Dashbord on the left nav")
