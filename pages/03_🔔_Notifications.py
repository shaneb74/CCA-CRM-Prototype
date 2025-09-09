
import streamlit as st
from ui.widgets import inject_css
from data_loader import load_seed

st.set_page_config(page_title="Notifications", page_icon="🔔", layout="wide")
inject_css()
data = load_seed()

if "dismissed" not in st.session_state: st.session_state.dismissed = []
if "filter_types" not in st.session_state:
    st.session_state.filter_types = {"Compliance": True, "Financial": True, "General": True}

st.title("🔔 Notifications")

with st.expander("Filters", expanded=True):
    f1,f2,f3 = st.columns(3)
    with f1: st.session_state.filter_types["Compliance"] = st.checkbox("Compliance", value=st.session_state.filter_types["Compliance"])
    with f2: st.session_state.filter_types["Financial"] = st.checkbox("Financial", value=st.session_state.filter_types["Financial"])
    with f3: st.session_state.filter_types["General"] = st.checkbox("General", value=st.session_state.filter_types["General"])

unread = [n for n in data["notifications"] if n["id"] not in st.session_state.dismissed]
hist = [n for n in data["notifications"] if n["id"] in st.session_state.dismissed]

st.subheader("Unread")
shown=False
for n in unread:
    if st.session_state.filter_types.get(n["type"], True):
        c1,c2 = st.columns([12,1])
        with c1:
            st.markdown(f"- {n['text']}  
  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)
        with c2:
            if st.button("✕", key=f"notif_{n['id']}"):
                st.session_state.dismissed.append(n["id"])
                shown=True
if not unread:
    st.caption("No unread.")

st.subheader("History")
shown=False
for n in hist:
    if st.session_state.filter_types.get(n["type"], True):
        st.markdown(f"- {n['text']}  
  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)
if not hist:
    st.caption("No history yet.")

st.page_link("pages/01_Advisor_Workspace.py", label="← Back to workspace")
