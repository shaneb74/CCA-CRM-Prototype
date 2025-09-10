# pages/00_Workflows.py
import streamlit as st
import store

st.set_page_config(page_title="Workflows", page_icon="🧭", layout="wide")

def go(label: str, path: str, key: str):
    # Prefer switch_page if available; otherwise, show a plain link
    if hasattr(st, "switch_page"):
        if st.button(label, key=key):
            st.switch_page(path)  # e.g. "pages/06_Intake_Workflow.py"
    else:
        # Fall back to a standard link. Do NOT st.write(None).
        st.markdown(f"[{label}]({path})")

lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None

st.title("Workflows")

if not lead:
    st.info("Select a client in Client Record first.")
    st.stop()

st.markdown(
    f"**Client:** {lead['name']} ({lead['id']}) • {lead['city']} • **Assigned:** {lead.get('assigned_to','Unassigned')}"
)

st.header("Intake")
st.caption("Collect personal, care, financial, lifestyle.")
go("Open Intake →", "pages/06_Intake_Workflow.py", key="open_intake")

st.header("Placement")
st.caption("Shortlist communities, schedule tours, record outcomes.")
go("Open Placement →", "pages/07_Placement_Workflow.py", key="open_place")

st.header("Follow-up")
st.caption("Post-placement check-ins and escalations.")
go("Open Follow-up →", "pages/08_Followup_Workflow.py", key="open_followup")