# 06_Intake_Workflow.py — guard: only assigned advisor can edit
import streamlit as st
import store

store.init()

lead_id = st.session_state.get("intake_lead_id") or store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Intake Workflow")
if not lead:
    st.info("No client selected for intake. Go back to Client Record and click Start Intake.")
    st.stop()

current_user = (getattr(store, "CURRENT_USER", "") or "").strip().lower()
assigned_to = (lead.get("assigned_to") or "").strip().lower()
mine = current_user == assigned_to

st.caption(f"Client: {lead['name']} ({lead['id']}) — {lead['city']} • Assigned: {lead.get('assigned_to') or 'Unassigned'}")

if not mine:
    st.error("Only the assigned advisor can run intake for this client.")
    if hasattr(st, "page_link"):
        st.page_link("pages/04_Client_Record.py", label="Back to Client Record →", icon="↩️")
    st.stop()

# ---- Normal intake UI (unchanged) ----
st.session_state.setdefault("intake_data", {})
draft = st.session_state["intake_data"].get(lead_id, {
    "contact": {"first_name":"", "last_name":"", "phone":"", "email":"", "best_time":""},
    "care_needs": {"adls":[], "memory": False, "mobility": "Independent"},
    "insurance": {"primary":"", "secondary":""},
    "notes": ""
})

with st.container(border=True):
    st.subheader("Contact")
    c1, c2 = st.columns(2)
    with c1:
        draft["contact"]["first_name"] = st.text_input("First name", value=draft["contact"]["first_name"] or lead["name"].split()[0])
        draft["contact"]["phone"] = st.text_input("Phone", value=draft["contact"]["phone"])
        draft["contact"]["best_time"] = st.selectbox("Best time to contact", ["", "Morning", "Afternoon", "Evening"], index=["","Morning","Afternoon","Evening"].index(draft["contact"]["best_time"]) if draft["contact"]["best_time"] in ["Morning","Afternoon","Evening"] else 0)
    with c2:
        last = lead["name"].split()[1] if len(lead["name"].split())>1 else ""
        draft["contact"]["last_name"] = st.text_input("Last name", value=draft["contact"]["last_name"] or last)
        draft["contact"]["email"] = st.text_input("Email", value=draft["contact"]["email"])

with st.container(border=True):
    st.subheader("Care needs")
    draft["care_needs"]["memory"] = st.checkbox("Memory support needed", value=draft["care_needs"]["memory"])
    draft["care_needs"]["mobility"] = st.selectbox("Mobility", ["Independent","Needs assistance","Wheelchair"], index=["Independent","Needs assistance","Wheelchair"].index(draft["care_needs"]["mobility"]))
    st.caption("Activities of Daily Living (pick all that apply)")
    adl_opts = ["Bathing","Dressing","Toileting","Transferring","Continence","Feeding"]
    selected = st.multiselect("ADLs", adl_opts, default=[a for a in (draft["care_needs"].get("adls") or []) if a in adl_opts])
    draft["care_needs"]["adls"] = selected

with st.container(border=True):
    st.subheader("Insurance")
    draft["insurance"]["primary"] = st.text_input("Primary insurance", value=draft["insurance"]["primary"])
    draft["insurance"]["secondary"] = st.text_input("Secondary insurance", value=draft["insurance"]["secondary"])

with st.container(border=True):
    st.subheader("Notes")
    draft["notes"] = st.text_area("Additional notes", value=draft["notes"], height=120)

st.session_state["intake_data"][lead_id] = draft

required = [draft["contact"]["first_name"], draft["contact"]["last_name"], draft["contact"]["phone"]]
filled = sum(1 for v in required if v.strip())
pct = max(store.get_progress(lead_id), filled / 3 * 0.6 + (0.2 if draft["care_needs"]["adls"] else 0))
st.progress(pct, text="Intake progress")

if st.button("Save progress"):
    store.set_progress(lead_id, pct)
    st.toast("Progress saved")

a1, a2 = st.columns([0.4,0.6])
with a1:
    if st.button("Complete Intake"):
        store.set_progress(lead_id, 1.0)
        lead["status"] = "in_progress"
        store.upsert_lead(lead)
        st.success("Intake completed.")
with a2:
    if st.button("Back to Client Record"):
        store.set_selected_lead(lead_id)
        if hasattr(st, "switch_page"):
            st.switch_page("pages/04_Client_Record.py")
        else:
            st.page_link("pages/04_Client_Record.py", label="Back to Client Record →", icon="↩️")
