# 04_Client_Record.py — DEBUG build CR-Debug-v5 2025-09-10T02:07:38.530053Z
import streamlit as st
import store

store.init()

st.title("Case Overview")
st.sidebar.warning("**BUILD:** CR-Debug-v5 2025-09-10T02:07:38.530053Z")
st.caption("If you don't see the BUILD banner in the sidebar, you're not on the file you think you are.")

# Debug switches
st.session_state.setdefault("show_intake_inline", False)
st.session_state.setdefault("client_search_q","")

leads_all = store.get_leads()

# Who am I
st.sidebar.info({
    "CURRENT_USER": getattr(store, "CURRENT_USER", None),
    "switch_page_available": hasattr(st, "switch_page"),
    "streamlit_version": getattr(st, "__version__", "unknown"),
})

# Advisor filter + search
agents = sorted({(l.get("assigned_to") or "").strip() for l in leads_all if l.get("assigned_to")}) or ["Unassigned"]
agent_filter = st.selectbox("Filter by advisor", ["All advisors"] + agents, index=0)
q = st.text_input("Search by first or last name", key="client_search_q", placeholder="e.g., John, Smith, Alvarez")

def _match_agent(l):
    return True if agent_filter == "All advisors" else (l.get("assigned_to") or "").strip() == agent_filter

def _match_name(l):
    return True if not q else q.strip().lower() in l["name"].lower()

filtered = [l for l in leads_all if _match_agent(l) and _match_name(l)]
if not filtered:
    st.stop()

# selection
current_id = store.get_selected_lead_id() or filtered[0]["id"]
if current_id not in [x["id"] for x in filtered]:
    current_id = filtered[0]["id"]
store.set_selected_lead(current_id)

options = {f"{x['name']} ({x['id']}) — {x['city']} — {x.get('assigned_to') or 'Unassigned'}": x["id"] for x in filtered}
idx = list(options.values()).index(current_id)
sel_label = st.selectbox("Matching clients", list(options.keys()), index=idx)
store.set_selected_lead(options[sel_label])

lead = store.get_lead(store.get_selected_lead_id())

# Header
st.markdown(f"### {lead['name']}")
st.caption(f"Assigned: {lead.get('assigned_to') or 'Unassigned'}  •  Lead ID: {lead['id']}")

# Assign gating — show exact comparison details
current_user = (getattr(store, "CURRENT_USER", "") or "").strip()
assigned_to = (lead.get("assigned_to") or "").strip()
mine = current_user.lower() == assigned_to.lower()
with st.expander("Debug: assignment check", expanded=False):
    st.write({
        "CURRENT_USER": current_user,
        "assigned_to": assigned_to,
        "equal_lower": mine,
    })

colA, colB, colC = st.columns([0.3,0.3,0.4])
with colA:
    if mine:
        st.success("Assigned to you")
    else:
        if st.button("Assign to me"):
            lead["assigned_to"] = current_user or "Unknown User"
            store.upsert_lead(lead)
            st.rerun()

def _start_intake():
    st.session_state["intake_lead_id"] = lead["id"]
    st.session_state["show_intake_inline"] = True

with colB:
    st.button("Start Intake", on_click=_start_intake)

with colC:
    st.caption("This page renders an inline intake for DEBUG.")

# Inline intake section
if st.session_state.get("show_intake_inline"):
    st.subheader("Intake (inline) — DEBUG")
    st.info("If you can read this, the new file is active and the Start Intake on_click worked.")
    st.text_input("Contact first name")
    st.text_input("Contact last name")
    st.text_area("Notes")
    if st.button("Close inline Intake"):
        st.session_state["show_intake_inline"] = False
        st.rerun()
