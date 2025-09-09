# pages/02_Advisor_Workspace.py
import streamlit as st
from data_loader import load_seed
from ui.widgets import inject_css, kpi, chips, tile

st.set_page_config(page_title="Advisor Workspace", page_icon="💼", layout="wide")
inject_css()
data = load_seed()

# ---------------- helpers ----------------
def get_client(cid):
    for c in data["clients"]:
        if c["id"] == cid:
            return c
    return data["clients"][0]

def select_client(cid):
    st.session_state["selected_client_id"] = cid
    st.rerun()

# One little per-client store so care needs / notes can be edited without a DB
def case_state(cid):
    if "case_store" not in st.session_state:
        st.session_state["case_store"] = {}
    if cid not in st.session_state["case_store"]:
        st.session_state["case_store"][cid] = {
            "needs": [],                # user-set list of care needs
            "note": "",                 # scratch note
            "intake_progress": 40,      # visual only
            "ds_result": None,          # decision support result (plan)
            "ds_cost": None,            # decision support cost
            "activities": [
                "Email: Disclosure sent 9/3",
                "Phone: Spoke with daughter 9/4",
                "Tour: Cedar Grove 9/7",
            ],
        }
    return st.session_state["case_store"][cid]

# ---------------- session defaults ----------------
if "selected_client_id" not in st.session_state:
    st.session_state["selected_client_id"] = data["clients"][0]["id"]

adv = data["advisors"][0]
mtd = sum(p["fee_amount"] for p in data["placements"] if p["advisor_id"] == adv["id"])
goal = adv["goal_monthly"]

# ---------------- top KPIs ----------------
k1, k2, k3, k4 = st.columns(4)
with k1: kpi("New leads (today)", "5")
with k2: kpi("Assigned leads", "12")
with k3: kpi("Active cases", str(len(data["clients"])))
with k4: kpi("MTD vs goal", f"${mtd:,.0f} / ${goal:,.0f}", f"{int(mtd/goal*100)}%")

chips(["Overdue: 2", "Tours this week: 3", "Docs pending: 1"])

# ---------------- layout: two columns ----------------
left, right = st.columns([1.1, 2.2])

# -------- left: Work Queue (click to load) ----------
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

# -------- right: Case Overview (wide) ---------------
cid = st.session_state["selected_client_id"]
case = get_client(cid)
store = case_state(cid)

with right:
    st.markdown("### Case Overview")
    st.markdown(f"**{case['name']}** • {case['city']}")
    chips([f"Stage: {case['stage']}", f"Priority: {case['priority']}", f"Budget: ${case['budget']:,.0f}"])

    # Quick note
    store["note"] = st.text_area("Quick note", value=store["note"], placeholder="Add a quick note...", height=80)

    # Intake progress
    st.markdown("#### Intake")
    store["intake_progress"] = st.slider("Progress", 0, 100, store["intake_progress"])
    st.progress(store["intake_progress"])

    # Care needs (replaces the confusing checkboxes)
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

    # Financials stub
    st.markdown("#### Financials")
    st.write("Monthly budget, assets, payer source. MTD goal contribution will calculate post-placement.")

    # Decision support results (display-only; launcher moved to left nav)
    st.markdown("#### Decision support (last results)")
    # Show what we have; if none, show helpful placeholders
    ds_plan = store["ds_result"] or {"plan": "—", "notes": "No result saved yet"}
    ds_cost = store["ds_cost"] or {"estimate": "—", "assumptions": "No estimate saved yet"}
    tile(f"Recommended: {ds_plan['plan']}", ds_plan.get("notes", ""))
    tile(f"Estimated Cost: {ds_cost['estimate']}", ds_cost.get("assumptions", ""))

    # Activities
    st.markdown("#### Activities")
    for a in store["activities"]:
        st.write(f"- {a}")
    new_act = st.text_input("Log new activity", "")
    if new_act:
        store["activities"].insert(0, new_act)
        st.session_state[f"clear_{cid}"] = ""  # noop anchor to trigger rerun
        st.rerun()
