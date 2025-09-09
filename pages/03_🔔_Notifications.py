
import streamlit as st
from ui.widgets import inject_css
inject_css()

# Boot session state if missing (in case user deep-links here first)
if "notifications" not in st.session_state:
    st.session_state.notifications = [
        {"id": 1, "type": "Compliance", "pill": "comp", "text": "Upload signed Disclosure before scheduling tours."},
        {"id": 2, "type": "Financial", "pill": "fin", "text": "Confirm Medicaid rollover during financial review."},
        {"id": 3, "type": "General", "pill": "gen", "text": "Keep intake notes date-stamped with initials."}
    ]
if "dismissed" not in st.session_state:
    st.session_state.dismissed = []

st.title("🔔 Notifications")

# Filters
if "filter_types" not in st.session_state:
    st.session_state.filter_types = {"Compliance": True, "Financial": True, "General": True}

with st.expander("Filters", expanded=True):
    f1,f2,f3 = st.columns(3)
    with f1: st.session_state.filter_types["Compliance"] = st.checkbox("Compliance", value=st.session_state.filter_types["Compliance"])
    with f2: st.session_state.filter_types["Financial"] = st.checkbox("Financial", value=st.session_state.filter_types["Financial"])
    with f3: st.session_state.filter_types["General"] = st.checkbox("General", value=st.session_state.filter_types["General"])

unread = [n for n in st.session_state.notifications if n["id"] not in st.session_state.dismissed]
history = [n for n in st.session_state.notifications if n["id"] in st.session_state.dismissed]

# Unread section
st.subheader("Unread")
shown = False
for n in unread:
    if st.session_state.filter_types.get(n["type"], True):
        shown = True
        col, col2 = st.columns([12,1])
        with col:
            st.markdown(f"- {n['text']}  \n  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)
        with col2:
            if st.button("✕", key=f"notif_dismiss_{n['id']}", help="Mark handled"):
                st.session_state.dismissed.append(n["id"])
if not shown:
    st.caption("No unread.")

# History section
st.subheader("History")
shown_h = False
for n in history:
    if st.session_state.filter_types.get(n["type"], True):
        shown_h = True
        st.markdown(f"- {n['text']}  \n  <span class='pill {n['pill']}'>{n['type']}</span>", unsafe_allow_html=True)
if not shown_h:
    st.caption("No history yet.")

# Return link
st.page_link("pages/01_Advisor_Dashboard_Mock.py", label="← Back to dashboard")
