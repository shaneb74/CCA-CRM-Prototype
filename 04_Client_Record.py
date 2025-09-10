# 04_Client_Record.py — assign button gated; Start Intake routes to workflow
import streamlit as st
from datetime import date
import store

store.init()

st.title("Case Overview")
st.markdown('<style>.page{max-width:1200px;margin:0 auto}.note{color:#6b7280}</style>', unsafe_allow_html=True)
st.markdown('<div class="page">', unsafe_allow_html=True)

# Ensure case_steps exists
st.session_state.setdefault("case_steps", {})

# --------- Filters: Agent first, then visible search ---------
leads_all = store.get_leads()
agents = sorted({l.get("assigned_to") for l in leads_all if l.get("assigned_to")}) or ["Unassigned"]
agent_filter = st.selectbox("Filter by advisor", ["All advisors"] + agents, index=0)

with st.container(border=True):
    st.caption("Search by first or last name")
    def _clear_search():
        st.session_state.client_search_q = ""
    q = st.text_input("", placeholder="Type to filter: e.g., John, Smith, Alvarez", key="client_search_q")
    if q:
        st.button("Show all clients", on_click=_clear_search)

def _match_agent(l):
    return True if agent_filter == "All advisors" else l.get("assigned_to") == agent_filter

def _match_name(l):
    return True if not q else q.strip().lower() in l["name"].lower()

filtered = [l for l in leads_all if _match_agent(l) and _match_name(l)]

# Selected lead handling
current_id = store.get_selected_lead_id()
if not current_id or not any(l["id"] == current_id for l in filtered):
    if filtered:
        current_id = filtered[0]["id"]
        store.set_selected_lead(current_id)

if filtered:
    options = {f"{x['name']} ({x['id']}) — {x['city']} — {x.get('assigned_to') or 'Unassigned'}": x["id"] for x in filtered}
    idx = list(options.values()).index(current_id) if current_id in options.values() else 0
    sel_label = st.selectbox("Matching clients", list(options.keys()), index=idx)
    store.set_selected_lead(options[sel_label])
else:
    st.info("No clients match your filter/search. Click 'Show all clients' to reset.")
    st.stop()

lead = store.get_lead(store.get_selected_lead_id())

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
    mine = (lead.get("assigned_to") == store.CURRENT_USER)
    if not lead.get("assigned_to"):
        st.warning("This client is unassigned.")
    if st.button("Assign to me", disabled=mine):
        if not mine:
            lead["assigned_to"] = store.CURRENT_USER
            store.upsert_lead(lead)
            st.success(f"Assigned to {store.CURRENT_USER}.")
            st.experimental_rerun()
with qa2:
    if st.button("Start Intake"):
        st.session_state["intake_lead_id"] = lead["id"]
        # move progress a notch to show motion in demo
        try:
            store.set_progress(lead["id"], max(store.get_progress(lead["id"]), 0.20))
        except Exception:
            pass
        if hasattr(st, "switch_page"):
            st.switch_page("pages/06_Intake_Workflow.py")
        else:
            st.experimental_rerun()
with qa3:
    st.caption("After tours, log results here and the pipeline will advance automatically.")

st.markdown('</div>', unsafe_allow_html=True)
