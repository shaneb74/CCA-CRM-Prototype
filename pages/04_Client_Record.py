# 04_Client_Record.py — attractive case overview
import streamlit as st, store
from datetime import date, timedelta
store.init()
def segmented(label, options, default):
    if hasattr(st, "segmented_control"):
        return st.segmented_control(label, options=options, default=default)
    return st.radio(label, options, index=options.index(default), horizontal=True)
def kpi_card(title, value, sub_html=""):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(f"<div class='num' style='font-size:28px;font-weight:700'>{value}</div>", unsafe_allow_html=True)
        if sub_html:
            st.markdown(f"<div class='sub'>{sub_html}</div>", unsafe_allow_html=True)
def badge(text, bg="#f3f4f6", fg="#374151"):
    st.markdown(f"<span class='badge' style='background:{bg};color:{fg}'> {text} </span>", unsafe_allow_html=True)

st.title("Case Overview")
st.markdown("""<style>\n  .page {max-width:1200px;margin:0 auto}\n  .card {background:#fff;border:1px solid #e9edf3;border-radius:16px;padding:18px}\n  .kpi h3 {margin:0;font-size:14px;color:#6b7280;font-weight:600}\n  .kpi .num {font-size:28px;font-weight:700;color:#111827;line-height:1}\n  .sub {font-size:12px;color:#6b7280}\n  .badge {display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid rgba(0,0,0,0.06)}\n  .badge.green {background:#ecfdf5;color:#065f46}\n  .badge.red {background:#fef2f2;color:#991b1b}\n  .badge.yellow {background:#fffbeb;color:#92400e}\n  .alert {background:#f7fbff;border:1px solid #e1f0ff;border-radius:12px;padding:10px 12px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center}\n  .alert .tag {font-size:11px;color:#2563eb;background:#eaf2ff;border-radius:999px;padding:2px 8px;margin-left:6px}\n  .section-title{font-weight:700;font-size:18px;margin:8px 0}\n  .task-title{font-weight:600;color:#111827;margin-bottom:2px}\n  .task-sub{font-size:12px;color:#6b7280}\n  .overdue{color:#b91c1c !important}\n</style>""", unsafe_allow_html=True)
st.markdown('<div class="page">', unsafe_allow_html=True)
lead_id = store.get_selected_lead_id()
lead = store.get_lead(lead_id) if lead_id else None
if not lead:
    options = {f"{x['name']} ({x['id']})": x["id"] for x in store.get_leads()}
    selected = st.selectbox("Select a lead", list(options.keys()))
    store.set_selected_lead(options[selected])
    lead = store.get_lead(store.get_selected_lead_id())
if lead["origin"] == "app":
    st.success(f"Origin: App Submission — Guided Care Plan completed on {lead['created'].isoformat()}")
elif lead["origin"] == "hospital":
    st.warning(f"Origin: Hospital Referral — created {lead['created'].isoformat()}")
else:
    st.info(f"Origin: {lead['origin'].title()} — created {lead['created'].isoformat()}")
h1, h2, h3, h4 = st.columns([0.35, 0.15, 0.25, 0.25])
with h1:
    st.markdown(f"### {{lead['name']}}")
    st.caption(lead["city"])
with h2:
    st.caption(f"Status: {{lead['status'].replace('_',' ').title()}}")
with h3:
    st.caption(f"Assigned: {{lead['assigned_to'] or 'Unassigned'}}")
with h4:
    st.caption(f"Lead ID: {{lead['id']}}")
st.divider()
c1, c2 = st.columns([0.55, 0.45])
with c1:
    st.subheader("Info from App")
    st.write(f"**Care Preference:** {{lead['preference']}}")
    if lead["budget"]: st.write(f"**Budget:** ${{lead['budget']:,}}/month")
    st.write(f"**Timeline:** {{lead['timeline']}}")
    if lead["notes"]: st.write(f"**Notes:** {{lead['notes']}}")
with c2:
    st.subheader("Next Steps")
    default_steps = [
        {"label": f"Call {{lead['name']}} within 24h", "key": "call"},
        {"label": "Upload Disclosure", "key": "disclosure"},
        {"label": "Complete Intake", "key": "intake"},
    ]
    for step in default_steps:
        key = f"{{lead['id']}}_{step['key']}"
        checked = st.session_state.case_steps.get(key, False)
        new = st.checkbox(step["label"], value=checked, key=key)
        st.session_state.case_steps[key] = new
st.divider()
qa1, qa2, qa3 = st.columns([0.25,0.25,0.5])
with qa1:
    if st.button("Assign to me"):
        lead["assigned_to"] = "Current Advisor"
        store.upsert_lead(lead)
        st.success("Assigned.")
with qa2:
    if st.button("Start Intake"):
        st.toast("Intake started.")
with qa3:
    st.caption("After tours, log results here and the pipeline will advance automatically.")
st.markdown('</div>', unsafe_allow_html=True)
