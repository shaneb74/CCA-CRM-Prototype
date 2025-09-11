# pages/04_Client_Record.py
from __future__ import annotations
import datetime
import streamlit as st

try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    pass

import store

# Intake progress
try:
    from Workflows.Intake.progress import show_intake_progress
    _intake_loaded = True
except Exception:
    show_intake_progress = None
    _intake_loaded = False

def _switch_page_hard(path: str):
    try:
        if hasattr(st, "switch_page"):
            st.switch_page(path)
            return
    except Exception:
        pass
    st.session_state["_goto_page"] = path
    st.rerun()

def _open_intake():
    lead = st.session_state.get("_lead_obj")
    if lead and lead.get("id"):
        store.set_selected_lead(lead["id"])
    for p in ("pages/90_Intake_Workflow.py", "pages/06_Intake_Workflow.py"):
        _switch_page_hard(p)

def _open_placement():
    lead = st.session_state.get("_lead_obj")
    if lead and lead.get("id"):
        store.set_selected_lead(lead["id"])
    _switch_page_hard("pages/91_Placement_Workflow.py")

def _assign_to_me():
    lead = st.session_state.get("_lead_obj")
    if not lead:
        return
    me = getattr(store, "CURRENT_USER", "Current Advisor")
    if lead.get("assigned_to") != me:
        lead["assigned_to"] = me
        store.upsert_lead(lead)
        st.success(f"Assigned to {me}")
        st.rerun()

store.init()
st.title("Case Overview")

leads = store.get_leads()
advisors = sorted({l.get("assigned_to") for l in leads if l.get("assigned_to")}) or ["Unassigned"]
advisor_filter = st.selectbox(
    "Filter by advisor",
    options=["All advisors"] + advisors,
    index=0,
    key="client_record_filter_advisor",
)
q = st.text_input("Search by first or last name", placeholder="Type to filter: e.g., John, Smith, Alvarez")

def _lead_label(l: dict) -> str:
    return f"{l.get('name','')} ({l.get('id','')}) — {l.get('city','')} — {l.get('assigned_to') or 'Unassigned'}"

filtered = []
for l in leads:
    if advisor_filter != "All advisors" and (l.get("assigned_to") or "Unassigned") != advisor_filter:
        continue
    if q and (q.lower() not in l.get("name","").lower()) and (q.lower() not in l.get("id","").lower()):
        continue
    filtered.append(l)

if not filtered and not q and advisor_filter == "All advisors":
    filtered = leads

lead_id_current = store.get_selected_lead_id()
options = [_lead_label(l) for l in filtered] or ["— no clients —"]
idx_default = 0
if lead_id_current:
    for i, l in enumerate(filtered):
        if l.get("id") == lead_id_current:
            idx_default = i
            break

sel = st.selectbox(
    "Matching clients",
    options=options,
    index=idx_default,
    key="client_record_match_select",
)

if filtered:
    selected = filtered[options.index(sel)]
    store.set_selected_lead(selected.get("id"))

lead = store.get_lead(store.get_selected_lead_id()) if store.get_selected_lead_id() else (filtered[0] if filtered else None)
st.session_state["_lead_obj"] = lead

if not lead:
    st.info("No matching clients. Adjust filters above.")
    st.stop()

origin = lead.get("origin", "App")
created_on = datetime.date.today().isoformat()
st.success(f"Origin: {str(origin).title()} — Guided Care Plan completed on {created_on}")

c1, c2, c3, c4 = st.columns([2,1,1,1])
with c1:
    st.subheader(lead.get("name",""))
    st.caption(lead.get("city",""))
with c2:
    st.caption("Status")
    st.write(lead.get("status","New"))
with c3:
    st.caption("Assigned")
    st.write(lead.get("assigned_to") or "Unassigned")
with c4:
    st.caption("Lead ID")
    st.write(lead.get("id","—"))

# Intake progress (and a tiny proof-of-life caption)
if show_intake_progress:
    show_intake_progress(lead)
else:
    st.caption("Intake progress module not found (Workflows/Intake/progress.py).")

st.divider()

lc1, lc2 = st.columns([2,2])
with lc1:
    st.subheader("Info from App")
    st.write(f"**Care Preference:** {lead.get('preference','—')}")
    budget = lead.get("budget", 0)
    if budget:
        st.write(f"**Budget:** ${int(budget):,}/month")
    else:
        st.write("**Budget:** —")
    st.write(f"**Timeline:** {lead.get('timeline','—')}")
    if lead.get("notes"):
        st.write(f"**Notes:** {lead.get('notes')}")

with lc2:
    st.subheader("Next Steps")
    st.checkbox(f"Call {lead.get('name','client')} within 24h", key="ns_call", value=False)
    st.checkbox("Upload Disclosure", key="ns_disclosure", value=False)
    st.checkbox("Complete Intake", key="ns_intake", value=False)

st.divider()

st.subheader("Decision Support")
dsr = lead.get("ds_recommendation") or lead.get("preference") or "—"
dsc = lead.get("ds_est_cost")
cost_str = f"${int(dsc):,} / month" if isinstance(dsc, (int, float)) and dsc > 0 else "—"
st.write(f"**Recommended:** {dsr}")
st.write(f"**Estimated cost:** {cost_str}")

btns = st.columns([1,1,1,6])
me = getattr(store, "CURRENT_USER", "Current Advisor")
already_mine = (lead.get("assigned_to") == me)
with btns[0]:
    st.button("Assign to me", on_click=_assign_to_me, disabled=already_mine, key="assign_to_me_btn")
with btns[1]:
    st.button("Start Intake", on_click=_open_intake, disabled=not already_mine, key="start_intake_btn")
with btns[2]:
    if st.button("Open Placement Workflow", key="open_placement_btn"):
        if lead and lead.get("id"):
            store.set_selected_lead(lead["id"])
        st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
        st.rerun()
st.caption("After tours, log results here and the pipeline will advance automatically.")