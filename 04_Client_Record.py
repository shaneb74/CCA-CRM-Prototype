# 04_Client_Record.py — inline-first intake (renders immediately), strict assign gating
import streamlit as st
import store

store.init()

st.title("Case Overview")
st.session_state.setdefault("case_steps", {})
st.session_state.setdefault("show_intake_inline", False)

# --------- Filters ---------
leads_all = store.get_leads()
agents = sorted({(l.get("assigned_to") or "").strip() for l in leads_all if l.get("assigned_to")}) or ["Unassigned"]
agent_filter = st.selectbox("Filter by advisor", ["All advisors"] + agents, index=0)

with st.container(border=True):
    st.caption("Search by first or last name")
    def _clear_search():
        st.session_state.client_search_q = ""
    q = st.text_input("", placeholder="Type to filter: e.g., John, Smith, Alvarez", key="client_search_q")
    if q:
        st.button("Show all clients", on_click=_clear_search)

def _match_agent(l):
    return True if agent_filter == "All advisors" else (l.get("assigned_to") or "").strip() == agent_filter

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
origin = lead.get("origin","").title()
st.info(f"Origin: {origin} — created {lead['created'].isoformat()}")

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

# ------ Details (hidden when intake inline is open) ------
if not st.session_state.show_intake_inline:
    c1, c2 = st.columns([0.55, 0.45])
    with c1:
        st.subheader("Info from App")
        st.write(f"**Care Preference:** {lead.get('preference','—')}")
        if lead.get("budget"):
            st.write(f"**Budget:** ${lead['budget']:,}/month")
        st.write(f"**Timeline:** {lead.get('timeline','—')}")
        if lead.get("notes"):
            st.write(f"**Notes:** {lead['notes']}")

    with c2:
        st.subheader("Next Steps")
        for step_key, label in [("call", f"Call {lead['name']} within 24h"),
                                ("disclosure", "Upload Disclosure"),
                                ("intake", "Complete Intake")]:
            key = f"{lead['id']}_{step_key}"
            st.session_state.case_steps[key] = st.checkbox(label, value=st.session_state.case_steps.get(key, False))

    st.divider()

    st.subheader("Decision Support")
    rec = lead.get("ds_recommendation", "Assisted Living")
    est = lead.get("ds_est_cost", 4500)
    st.markdown(f"**Recommended:** {rec}")
    st.markdown(f"**Estimated cost:** ${est:,.0f} / month")

# ------ Footer actions ------
qa1, qa2, qa3 = st.columns([0.25,0.25,0.5])
with qa1:
    mine = ( (lead.get("assigned_to") or "").strip().lower() == (store.CURRENT_USER or "").strip().lower() )
    if mine:
        st.success("Assigned to you")
    else:
        if st.button("Assign to me"):
            lead["assigned_to"] = store.CURRENT_USER
            store.upsert_lead(lead)
            st.success(f"Assigned to {store.CURRENT_USER}.")
            st.session_state.show_intake_inline = False  # keep normal view
            st.experimental_rerun()

with qa2:
    start_now = st.button("Start Intake")
    if start_now:
        st.session_state["intake_lead_id"] = lead["id"]
        # show intake immediately, no reliance on rerun or switch_page
        st.session_state.show_intake_inline = True
        try:
            store.set_progress(lead["id"], max(store.get_progress(lead["id"]), 0.20))
        except Exception:
            pass
        st.toast("Intake started")

with qa3:
    st.caption("After tours, log results here and the pipeline will advance automatically.")

# ------ Inline intake (renders immediately when Start Intake clicked) ------
if st.session_state.show_intake_inline:
    st.divider()
    st.subheader("Intake")
    st.caption("Inline intake shown here. You can also open the full Intake page below.")

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

    b1, b2 = st.columns([0.4,0.6])
    with b1:
        if st.button("Open full Intake page →"):
            if hasattr(st, "switch_page"):
                st.switch_page("pages/06_Intake_Workflow.py")
            else:
                st.page_link("pages/06_Intake_Workflow.py", label="Open Intake Workflow", icon="🧭")
    with b2:
        if st.button("Close inline Intake"):
            st.session_state.show_intake_inline = False
            st.experimental_rerun()
