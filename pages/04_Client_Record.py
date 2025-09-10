# 04_Client_Record.py — Client search with 'Show all clients' clear control
import streamlit as st
from datetime import date
import store

store.init()

st.title("Case Overview")

# Styles
st.markdown('<style>.page{max-width:1200px;margin:0 auto}.note{color:#6b7280}</style>', unsafe_allow_html=True)
st.markdown('<div class="page">', unsafe_allow_html=True)

# Ensure case_steps exists
if "case_steps" not in st.session_state:
    st.session_state.case_steps = {}

# ------ Search UI ------
st.subheader("Find a client")

def _clear_search():
    st.session_state.client_search_q = ""

q = st.text_input(
    "Search by first or last name",
    placeholder="Type to filter: e.g., John, Smith, Alvarez",
    key="client_search_q",
)

# Toolbar: show a 'Show all clients' button when there's an active query
toolbar_cols = st.columns([0.75, 0.25])
with toolbar_cols[1]:
    if q:
        st.button("Show all clients", on_click=_clear_search)

leads = store.get_leads()

def _matches(lead, q):
    if not q:
        return True
    ql = q.strip().lower()
    return ql in lead["name"].lower()

filtered = [l for l in leads if _matches(l, q)]

# Selected lead logic
current_id = store.get_selected_lead_id()
# If no selection or selection not in filtered (or list empty), pick first filtered
if not current_id or not any(l["id"] == current_id for l in filtered):
    if filtered:
        current_id = filtered[0]["id"]
        store.set_selected_lead(current_id)

# Let user switch among filtered results
if filtered:
    options = {f"{x['name']} ({x['id']}) — {x['city']}": x["id"] for x in filtered}
    idx = list(options.values()).index(current_id) if current_id in options.values() else 0
    sel_label = st.selectbox("Matching clients", list(options.keys()), index=idx)
    store.set_selected_lead(options[sel_label])
else:
    st.info("No clients match your search. Click 'Show all clients' to reset.")

lead = store.get_lead(store.get_selected_lead_id()) if filtered else None
if not lead:
    st.stop()

# ------ Header summary ------
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

# ------ Two-column detail ------
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

# Decision support block
st.subheader("Decision Support")
rec = lead.get("ds_recommendation", "Assisted Living")
est = lead.get("ds_est_cost", 4500)
st.markdown(f"**Recommended:** {rec}")
st.markdown(f"**Estimated cost:** ${est:,.0f} / month")

# Footer actions
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
