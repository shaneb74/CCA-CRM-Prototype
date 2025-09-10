
from ui_chrome import apply_chrome
import store
import streamlit as st
apply_chrome()
store.init()

st.title("Notifications")
items = store.get_notifications()
if not items:
    st.info("No new notifications.")
else:
    for n in items:
        st.info(n["text"])
