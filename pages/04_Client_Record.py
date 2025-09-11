
# pages/04_Client_Record.py
# Case Overview (Client Record) with stable navigation into Intake Workflow
from __future__ import annotations
import streamlit as st
import datetime
import store

# --- simple redirect consumer (kept local so this page works standalone) ---
def _consume_redirect_once():
    dest = st.session_state.pop("_goto_page", None)
    if dest and hasattr(st, "switch_page"):
        try:
            st.switch_page(dest)
        except Exception:
            pass

st.set_page_config(page_title="Case Overview", page_icon="📄", layout="wide")
_consume_redirect_once()
store.init()

st.title("Case Overview")

leads = store.get_leads()
if not leads:
    st.info("No clients available.")
    st.stop()

# pick currently selected lead or default to first
lead_id_current = store.get_selected_lead_id() or leads[0]["id"]
lead_ids = [l["id"] for l in leads]
labels = [f"{l['name']} ({l['id']}) — {l.get('city','')}" for l in leads]
idx = max(0, lead_ids.index(lead_id_current)) if lead_id_current in lead_ids else 0

sel = st.selectbox("Matching clients", labels, index=idx, key="client_record_match_select")
lead = leads[labels.index(sel)]
store.set_selected_lead(lead["id"])

# banner
st.success(f"Origin: {str(lead.get('origin','App')).title()} — Intake progress {int((lead.get('progress') or 0.0)*100)}%")

# header
c1,c2,c3,c4 = st.columns([2,1,1,1])
with c1:
    st.subheader(lead.get("name",""))
    st.caption(lead.get("city",""))
with c2:
    st.caption("Status"); st.write(lead.get("status","New"))
with c3:
    st.caption("Assigned"); st.write(lead.get("assigned_to") or "Unassigned")
with c4:
    st.caption("Lead ID"); st.write(lead.get("id","—"))

st.divider()

# Decision Support summary
lc1, lc2 = st.columns([2,2])
with lc1:
    st.subheader("Info from App")
    st.write(f"**Care Preference:** {lead.get('preference','—')}")
    budget = lead.get("budget", 0)
    st.write(f"**Budget:** {'${:,}/month'.format(int(budget)) if budget else '—'}")
    st.write(f"**Timeline:** {lead.get('timeline','—')}")
    if lead.get("notes"):
        st.write(f"**Notes:** {lead.get('notes')}")

with lc2:
    st.subheader("Next Steps")
    st.checkbox(f"Call {lead.get('name','client')} within 24h", key="ns_call", value=False)
    st.checkbox("Upload Disclosure", key="ns_disclosure", value=False)
    st.checkbox("Complete Intake", key="ns_intake", value=False)

st.divider()

# Navigation buttons (NO callbacks, we route inline so st.rerun isn't used inside callbacks)
b1, b2, b3 = st.columns([1,1,6])
with b1:
    if st.button("Start Intake", key="start_intake_btn"):
        store.set_selected_lead(lead["id"])
        # schedule redirect safely; intake page will consume it on the next run
        st.session_state["_goto_page"] = "pages/90_Intake_Workflow.py"
        st.experimental_rerun()
with b2:
    if st.button("Assign to me", key="assign_to_me_btn"):
        me = getattr(store, "CURRENT_USER", "Current Advisor")
        if lead.get("assigned_to") != me:
            lead["assigned_to"] = me
            store.upsert_lead(lead)
            st.success(f"Assigned to {me}")
            st.experimental_rerun()
# end
