# 04_Client_Record.py — hardened against missing session keys
import streamlit as st
from datetime import date
import store

store.init()  # ensure session keys exist

st.title("Case Overview")

# soft styles
st.markdown(
    '<style>.page{max-width:1200px;margin:0 auto}.note{color:#6b7280}</style>',
    unsafe_allow_html=True,
)
st.markdown('<div class="page">', unsafe_allow_html=True)

# Ensure case_steps exists even if store.init changes in the future
if "case_steps" not in st.session_state:
    st.session_state.case_steps = {}

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None
if not lead:
    options = {f"{x['name']} ({x['id']})": x["id"] for x in store.get_leads()}
    selected = st.selectbox("Select a lead", list(options.keys()))
    store.set_selected_lead(options[selected])
    lead = store.get_lead(store.get_selected_lead_id())

if lead["origin"] == "app":
    st.success(f"Origin: App Submission — Guided Care Plan completed on {lead['created'].isoformat()}")
elif lead["origin"] == "hospital":
    st.warning(f"Origin: Hospital Referral — created {lead['created'].isoformat()}")
else:
    st.info(f"Origin: {lead['origin'].title()} — created {lead['created'].isoformat()}")

h1, h2, h3, h4 = st.columns([0.35, 0.15, 0.25, 0.25])
with h1:
    st.markdown(f"### {lead['name']}")
    st.caption(lead["city"])
with h2:
    st.caption(f"Status: {lead['status'].replace('_',' ').title()}")
with h3:
    st.caption(f"Assigned: {lead['assigned_to'] or 'Unassigned'}")
with h4:
    st.caption(f"Lead ID: {lead['id']}")

st.divider()

c1, c2 = st.columns([0.55, 0.45])
with c1:
    st.subheader("Info from App")
    st.write(f"**Care Preference:** {lead['preference']}")
    if lead["budget"]:
        st.write(f"**Budget:** ${lead['budget']:,}/month")
    st.write(f"**Timeline:** {lead['timeline']}")
    if lead["notes"]:
        st.write(f"**Notes:** {lead['notes']}")

with c2:
    st.subheader("Next Steps")
    default_steps = [
        {"label": f"Call {lead['name']} within 24h", "key": "call"},
        {"label": "Upload Disclosure", "key": "disclosure"},
        {"label": "Complete Intake", "key": "intake"},
    ]
    for step in default_steps:
        key = f"{lead['id']}_{step['key']}"
        checked = st.session_state.case_steps.get(key, False)
        new = st.checkbox(step["label"], value=checked, key=key)
        st.session_state.case_steps[key] = new

st.divider()

qa1, qa2, qa3 = st.columns([0.25,0.25,0.5])
with qa1:
    if st.button("Assign to me"):
        lead["assigned_to"] = "Current Advisor"
        store.upsert_lead(lead)
        st.success("Assigned.")
with qa2:
    if st.button("Start Intake"):
        st.toast("Intake started.")
with qa3:
    st.caption("After tours, log results here and the pipeline will advance automatically.")

st.markdown('</div>', unsafe_allow_html=True)
