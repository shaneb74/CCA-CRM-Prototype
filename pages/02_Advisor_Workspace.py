import streamlit as st
from data_loader import load_seed
from ui.widgets import inject_css, chips, tile

st.set_page_config(page_title="Advisor Workspace", layout="wide")
inject_css()
data = load_seed()

# ---------- helpers ----------
def get_client(cid):
    for c in data["clients"]:
        if c["id"] == cid:
            return c
    return data["clients"][0]

def select_client(cid):
    st.session_state["selected_client_id"] = cid
    st.rerun()

def case_state(cid):
    if "case_store" not in st.session_state:
        st.session_state["case_store"] = {}
    if cid not in st.session_state["case_store"]:
        # defaults per case
        st.session_state["case_store"][cid] = {
            "needs": [],
            "note": "",
            "intake_progress": 40,  # visual only, rule-driven later
            # DS results now display-only with your example defaults
            "ds_result": {"plan": "Assisted Living", "notes": "Recommended based on care needs"},
            "ds_cost": {"estimate": "$8,000/mo", "assumptions": "Room, care tier, meds mgmt"},
            "activities": [
                "Email: Disclosure sent 9/3",
                "Phone: Spoke with daughter 9/4",
                "Tour: Cedar Grove 9/7",
            ],
        }
    return st.session_state["case_store"][cid]

# ---------- session defaults ----------
if "selected_client_id" not in st.session_state:
    st.session_state["selected_client_id"] = load_seed()["clients"][0]["id"]

# ---------- layout: two columns ----------
left, right = st.columns([1.1, 2.2])

# === Left: Work Queue ===
with left:
    st.markdown("### Work Queue")
    _view = st.selectbox("Filter", options=["My leads", "All", "Overdue", "Tours"], index=0)

    for c in data["clients"]:
        is_sel = c["id"] == st.session_state["selected_client_id"]
        row = st.container()
        with row:
            c1, c2 = st.columns([0.8, 0.2])
            with c1:
                st.markdown(
                    f"**{c['name']}** — {c['stage']}  \n"
                    f"<span class='muted small'>{c['city']} • Next: {c['next']}</span>",
                    unsafe_allow_html=True,
                )
            with c2:
                label = "Selected" if is_sel else "Open"
                if st.button(label, key=f"open_{c['id']}", use_container_width=True, disabled=is_sel):
                    select_client(c["id"])
        st.divider()

# === Right: Case Overview (wide) ===
cid = st.session_state["selected_client_id"]
case = get_client(cid)
store = case_state(cid)

with right:
    st.markdown("### Case Overview")
    st.markdown(f"**{case['name']}** • {case['city']}")
    chips([f"Stage: {case['stage']}", f"Priority: {case['priority']}", f"Budget: ${case['budget']:,.0f}"])

    # Quick note (lightweight edit)
    store["note"] = st.text_area("Quick note", value=store["note"], placeholder="Add a quick note...", height=80)

    # Intake progress (status bar only; no slider)
    st.markdown("#### Intake")
    st.progress(store["intake_progress"])

    # Care needs (simple flags; replaces old confusing checkboxes)
    st.markdown("#### Care needs")
    needs = st.multiselect(
        "Select applicable needs",
        options=["Cognition support", "Mobility assistance", "Medication mgmt", "Behavioral support", "ADL support"],
        default=store["needs"],
        label_visibility="collapsed",
    )
    store["needs"] = needs
    if needs:
        chips(needs)

    # Financials (stub)
    st.markdown("#### Financials")
    st.write("Monthly budget, assets, payer source. MTD goal contribution will calculate post-placement.")

    # Decision support results (display-only here)
    st.markdown("#### Decision support (last results)")
    ds_plan = store["ds_result"]
    ds_cost = store["ds_cost"]
    tile(f"Recommended: {ds_plan['plan']}", ds_plan.get("notes", ""))
    tile(f"Estimated Cost: {ds_cost['estimate']}", ds_cost.get("assumptions", ""))

    # Activities log
    st.markdown("#### Activities")
    for a in store["activities"]:
        st.write(f"- {a}")
    new_act = st.text_input("Log new activity", key=f"add_act_{cid}")
    if new_act:
        store["activities"].insert(0, new_act)
        st.rerun()

    # Open full record button
    if st.button("Open full record", use_container_width=False):
        st.session_state["selected_client_id"] = cid
        try:
            # Streamlit 1.29+
            st.switch_page("pages/03_Client_Record.py")
        except Exception:
            st.info("Open the 'Client Record' page from the left navigation.")