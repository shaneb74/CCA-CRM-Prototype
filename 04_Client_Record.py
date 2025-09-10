# 04_Client_Record.py — stronger nav + inline intake fallback + proper assign gating
import streamlit as st
from datetime import date
import store

store.init()

st.title("Case Overview")
st.markdown('<style>.page{max-width:1200px;margin:0 auto}.note{color:#6b7280}</style>', unsafe_allow_html=True)
st.markdown('<div class="page">', unsafe_allow_html=True)

st.session_state.setdefault("case_steps", {})
st.session_state.setdefault("show_intake_inline", False)

# --------- Filters ---------
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

# ------ Two-column detail (skip if inline intake showing) ------
if not st.session_state.show_intake_inline:
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
    # Show status text and only render button when action is valid
    if mine:
        st.success("Assigned to you")
    else:
        if st.button("Assign to me"):
            lead["assigned_to"] = store.CURRENT_USER
            store.upsert_lead(lead)
            st.success(f"Assigned to {store.CURRENT_USER}.")
            st.experimental_rerun()

with qa2:
    if st.button("Start Intake"):
        st.session_state["intake_lead_id"] = lead["id"]
        try:
            store.set_progress(lead["id"], max(store.get_progress(lead["id"]), 0.20))
        except Exception:
            pass
        # Try real navigation first
        if hasattr(st, "switch_page"):
            try:
                st.switch_page("pages/06_Intake_Workflow.py")
            except Exception:
                st.session_state.show_intake_inline = True
                st.experimental_rerun()
        else:
            # Fallback to inline workflow
            st.session_state.show_intake_inline = True
            st.experimental_rerun()

with qa3:
    st.caption("After tours, log results here and the pipeline will advance automatically.")

# -------- Inline intake fallback (renders if nav not supported) --------
if st.session_state.show_intake_inline:
    st.divider()
    st.subheader("Intake (inline)")
    # very small inline form; for full experience use the dedicated page
    st.info("Navigation to the Intake page was unavailable, so you're seeing the inline fallback.")

    st.session_state.setdefault("intake_data", {})
    draft = st.session_state["intake_data"].get(lead["id"], {
        "contact": {"first_name":"", "last_name":"", "phone":"", "email":""},
        "care_needs": {"memory": False, "mobility": "Independent", "adls":[]},
        "insurance": {"primary":"", "secondary":""},
        "notes": ""
    })
    c1, c2 = st.columns(2)
    with c1:
        draft["contact"]["first_name"] = st.text_input("First name", value=draft["contact"]["first_name"] or lead["name"].split()[0])
        draft["contact"]["phone"] = st.text_input("Phone", value=draft["contact"]["phone"])
        draft["insurance"]["primary"] = st.text_input("Primary insurance", value=draft["insurance"]["primary"])
    with c2:
        last = lead["name"].split()[1] if len(lead["name"].split())>1 else ""
        draft["contact"]["last_name"] = st.text_input("Last name", value=draft["contact"]["last_name"] or last)
        draft["contact"]["email"] = st.text_input("Email", value=draft["contact"]["email"])
        draft["insurance"]["secondary"] = st.text_input("Secondary insurance", value=draft["insurance"]["secondary"])

    st.session_state["intake_data"][lead["id"]] = draft

    cols = st.columns([0.3,0.3,0.4])
    with cols[0]:
        if st.button("Open full Intake page →"):
            if hasattr(st, "switch_page"):
                st.switch_page("pages/06_Intake_Workflow.py")
            else:
                st.warning("Use the sidebar to open 'Intake Workflow'")

st.markdown('</div>', unsafe_allow_html=True)
