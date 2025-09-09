# pages/04_Client_Record.py
import streamlit as st
from data_loader import load_seed
from ui.widgets import inject_css, chips, tile

st.set_page_config(page_title="Client Record", layout="wide")
inject_css()
data = load_seed()

def get_client(cid):
    for c in data["clients"]:
        if c["id"] == cid:
            return c
    return data["clients"][0]

cid = st.session_state.get("selected_client_id", data["clients"][0]["id"])
case = get_client(cid)
store = st.session_state.get("case_store", {}).get(cid, {
    "needs": [],
    "note": "",
    "intake_progress": 40,
    "ds_result": {"plan": "Assisted Living", "notes": "Recommended based on care needs"},
    "ds_cost": {"estimate": "$8,000/mo", "assumptions": "Room, care tier, meds mgmt"},
    "activities": [],
})

st.markdown("### Client Record")
st.markdown(f"**{case['name']}** • {case['city']}")
chips([f"Stage: {case['stage']}", f"Priority: {case['priority']}", f"Budget: ${case['budget']:,.0f}"])

c1, c2 = st.columns([1.2, 1.8])
with c1:
    st.markdown("#### Snapshot")
    st.write(f"Referral source: {case.get('referral', '—')}")
    st.write(f"Next action: {case.get('next', '—')}")
    st.write("Care needs:")
    for n in store.get("needs", []):
        st.write(f"- {n}")

    st.markdown("#### Decision support (last results)")
    tile(f"Recommended: {store['ds_result']['plan']}", store['ds_result'].get("notes", ""))
    tile(f"Estimated Cost: {store['ds_cost']['estimate']}", store['ds_cost'].get("assumptions", ""))

with c2:
    st.markdown("#### Notes")
    st.text_area("Notes", value=store.get("note", ""), height=160)

    st.markdown("#### Intake progress")
    st.progress(store.get("intake_progress", 40))

    st.markdown("#### Activities")
    for a in store.get("activities", []):
        st.write(f"- {a}")

# Back to workspace
try:
    st.page_link("pages/02_Advisor_Workspace.py", label="← Back to Advisor Workspace")
except Exception:
    if st.button("Back to Advisor Workspace"):
        try:
            st.switch_page("pages/02_Advisor_Workspace.py")
        except Exception:
            st.info("Use the left navigation to return to Advisor Workspace.")