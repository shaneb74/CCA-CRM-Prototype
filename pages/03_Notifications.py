# 03_Notifications.py — simple alerts (defensive init)
import streamlit as st
import store
store.init()

def segmented(label, options, default):
    # Use segmented_control if available; otherwise fall back to radio
    if hasattr(st, "segmented_control"):
        return st.segmented_control(label, options=options, default=default)
    else:
        return st.radio(label, options, index=options.index(default), horizontal=True)


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
