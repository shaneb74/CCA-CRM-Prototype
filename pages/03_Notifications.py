import streamlit as st
import store

st.title("Notifications")

alerts = [
    ("Compliance", "Upload signed Disclosure before scheduling tours."),
    ("Financial", "Confirm Medicaid rollover during financial review."),
    ("General", "Keep intake notes date-stamped with initials."),
]
for idx, (tag, msg) in enumerate(alerts, start=1):
    c1, c2 = st.columns([0.9, 0.1])
    with c1:
        st.info(f"[{tag}] {msg}")
    with c2:
        st.button("✓", key=f"ack_{idx}")
