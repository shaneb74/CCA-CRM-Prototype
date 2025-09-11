# pages/89_Workflows.py — Workflows hub (minimal edit: fix "Open Intake" CTA navigation)
from __future__ import annotations
import streamlit as st

# Optional: consume pending redirect and set layout
try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    pass

import store

st.set_page_config(page_title="Workflows", page_icon="🗂", layout="wide")
store.init()

st.title("Workflows")

lead_id = store.get_selected_lead_id()
if not lead_id:
    st.info("Select a client in Client Record first.")
    st.stop()

lead = store.get_lead(lead_id) or {}

def _go_intake(lead_id: str):
    if not lead_id:
        return
    store.set_selected_lead(lead_id)
    st.session_state["_goto_page"] = "pages/90_Intake_Workflow.py"
    try:
        if hasattr(st, "switch_page"):
            st.switch_page("pages/90_Intake_Workflow.py")
    except Exception:
        pass

def _go_placement(lead_id: str):
    if not lead_id:
        return
    store.set_selected_lead(lead_id)
    st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
    try:
        if hasattr(st, "switch_page"):
            st.switch_page("pages/91_Placement_Workflow.py")
    except Exception:
        pass

c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("Intake")
    st.caption("Collect personal, care, financial, lifestyle.")
    st.button("Open Intake →", key="open_intake_wf", on_click=_go_intake, args=(lead_id,))
with c2:
    st.subheader("Placement")
    st.caption("Shortlist communities, schedule tours, record outcomes.")
    st.button("Open Placement →", key="open_place_wf", on_click=_go_placement, args=(lead_id,))
with c3:
    st.subheader("Follow-up")
    st.caption("Post-placement check-ins and escalations.")
    st.write("Use the Follow-up page from the sidebar once placement is complete.")
