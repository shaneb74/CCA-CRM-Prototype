# --- path bootstrap so root modules import from /pages scripts ---
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# optional chrome tweaks (safe if missing)
try:
    from ui_chrome import hide_default
    hide_default()
except Exception:
    pass

    import streamlit as st
    import store

    st.set_page_config(page_title="Intake Workflow", page_icon="🧾", layout="wide")
    store.init()
    lead_id = store.get_selected_lead_id()
    st.title("Intake Workflow")

    if not lead_id:
        st.info("No client selected. Use **Client Record** or the **Workflows** hub.")
        st.stop()

    lead = store.get_lead(lead_id)
    if not lead:
        st.error(f"Selected client '{lead_id}' not found.")
        st.stop()

    st.caption(f"{lead['name']} • {lead.get('city','–')} • **Assigned:** {lead.get('assigned_to','–')}")

    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([2,1,1,1])
        with c1:
            st.text_input("Full name", value=lead.get("name",""), key="intake_name", label_visibility="visible")
        with c2:
            st.text_input("Status", value=str(lead.get("status","")).replace("_"," ").title(), key="intake_status")
        with c3:
            st.number_input("Budget / mo", value=float(lead.get("budget",0)), step=100.0, key="intake_budget")
        with c4:
            st.text_input("Priority", value=str(lead.get("priority","")).title(), key="intake_priority")

    st.write("")
    if st.button("← Back to Workflows"):
        if hasattr(st, "switch_page"):
            st.switch_page("pages/89_Workflows.py")
