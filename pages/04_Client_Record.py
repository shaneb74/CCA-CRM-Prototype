# pages/04_Client_Record.py — Case Overview (patch: safe Start Intake navigation helper)
from __future__ import annotations
import streamlit as st
import datetime

try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    pass

import store

# --- helpers ---
def _go_intake_from_record():
    lead = st.session_state.get("_lead_obj") or {}
    lid = lead.get("id") or store.get_selected_lead_id()
    if lid:
        store.set_selected_lead(lid)
        st.session_state["_goto_page"] = "pages/90_Intake_Workflow.py"
        try:
            if hasattr(st, "switch_page"):
                st.switch_page("pages/90_Intake_Workflow.py")
        except Exception:
            pass

# --- original page scaffolding (kept minimal to not override your design) ---
st.set_page_config(page_title="Case Overview", page_icon="📄", layout="wide")
store.init()

# The rest of your original Case Overview content should remain here.
# This patch only provides `_go_intake_from_record()` so you can use it
# in your existing "Start Intake" button:
#
# st.button("Start Intake", on_click=_go_intake_from_record, key="start_intake_btn")
#
# Nothing else is altered to preserve your design.
st.caption("Patch loaded: use `_go_intake_from_record` in your Start Intake button.")
