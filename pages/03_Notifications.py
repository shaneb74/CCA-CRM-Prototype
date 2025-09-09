
import streamlit as st, json, os
from ui.widgets import inject_css, card

inject_css()
st.title("Notifications Center")

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notifications.json")
try:
    items = json.load(open(data_path))
except Exception:
    items = []

st.subheader("Unread")
if not items:
    st.caption("You're all caught up.")
for i, n in enumerate(items):
    text = n.get("text","")
    ntype = n.get("type","General")
    with card(None):
        st.write(text)
        st.caption(ntype)

st.subheader("History")
st.caption("Shown for demo only.")
for i, n in enumerate(items):
    with card(None):
        st.write(n.get("text",""))
        st.caption(n.get("type","General"))
