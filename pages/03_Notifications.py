
import streamlit as st
from ui.widgets import inject_css

st.set_page_config(page_title="Notifications", page_icon="🔔", layout="wide")
inject_css()

if "notifications" not in st.session_state:
    st.session_state.notifications = []
if "dismissed" not in st.session_state:
    st.session_state.dismissed = []

st.title("Notifications Center")

unread = [n for n in st.session_state.get("notifications", []) if n["id"] not in st.session_state.dismissed]
hist = [n for n in st.session_state.get("notifications", []) if n["id"] in st.session_state.dismissed]

st.subheader("Unread")
for n in unread:
    c1,c2 = st.columns([12,1])
    with c1: st.markdown(f"- {n['text']}  \n  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)
    with c2:
        if st.button("✕", key=f"notif_{n['id']}"): st.session_state.dismissed.append(n["id"])

st.subheader("History")
for n in hist:
    st.markdown(f"- {n['text']}  \n  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)
