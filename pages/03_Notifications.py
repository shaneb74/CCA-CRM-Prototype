
import streamlit as st
from ui.widgets import inject_css

inject_css()
st.markdown("## Notifications Center")

st.session_state.setdefault("notice_history", [])
st.session_state.setdefault("notices", [
    {"text":"Upload signed Disclosure before scheduling tours.", "type":"Compliance"},
    {"text":"Confirm Medicaid rollover during financial review.", "type":"Financial"},
    {"text":"Keep intake notes date-stamped with initials.", "type":"General"},
])

st.markdown("### Unread")
for n in st.session_state["notices"]:
    st.write(n["text"])
    st.caption(n["type"])

st.markdown("### History")
if not st.session_state["notice_history"]:
    st.caption("Shown for demo only.")
for n in st.session_state["notice_history"]:
    st.write(n["text"])
    st.caption(n["type"])
