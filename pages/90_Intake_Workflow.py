# pages/90_Intake_Workflow.py
from __future__ import annotations
import streamlit as st
try:
    import store
except Exception:
    store = None
try:
    st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
except Exception:
    pass
lead_id = None
lead = None
if store:
    try:
        lead_id = store.get_selected_lead_id()
        lead = store.get_lead(lead_id) if lead_id else None
    except Exception:
        pass
name=(lead or {}).get("name","—"); city=(lead or {}).get("city","—"); status=(lead or {}).get("status","—")
budget=(lead or {}).get("budget",None); timeline=(lead or {}).get("timeline","—"); assigned=(lead or {}).get("assigned_to","—")
st.title("Intake Workflow")
cc1,cc2,cc3,cc4=st.columns([2,1,1,1])
with cc1: st.markdown(f"**{name}** · {city}"); st.caption(f"Assigned: {assigned}")
with cc2: st.caption("Status"); st.write(str(status).replace("_"," ").title())
with cc3: st.caption("Budget / mo"); st.write(f"${int(budget):,}" if isinstance(budget,(int,float)) and budget>0 else "—")
with cc4: st.caption("Timeline"); st.write(timeline or "—")
st.divider()
INTAKE_STEPS=["Lead received","Lead assigned","Initial contact attempted","Initial contact made","Consultation scheduled","Assessment started","Assessment completed","Qualification decision"]
steps_key=f"intake_steps::{lead_id or 'unknown'}"
if steps_key not in st.session_state: st.session_state[steps_key]={s:(i==0) for i,s in enumerate(INTAKE_STEPS)}
is_done=st.session_state[steps_key]
pct=sum(1 for v in is_done.values() if v)/len(INTAKE_STEPS) if INTAKE_STEPS else 0.0
st.progress(pct)
pill_cols=st.columns(len(INTAKE_STEPS),gap="small")
for i,step in enumerate(INTAKE_STEPS):
    with pill_cols[i]:
        done=is_done.get(step,False)
        cls="pill pill--done" if done else ("pill pill--current" if i==sum(1 for v in is_done.values() if v) else "pill")
        st.markdown(f'<div class="{cls}">{step}</div>', unsafe_allow_html=True)
st.markdown("<style>.pill{border:1px solid #e5e7eb;border-radius:18px;padding:6px 10px;font-size:12px;text-align:center;color:#111827;background:#fff}.pill--done{background:#eef2ff;border-color:#c7d2fe}.pill--current{background:#f1f5f9;border-color:#cbd5e1}</style>", unsafe_allow_html=True)
left,right=st.columns([1.1,0.9])
with left:
    for step in INTAKE_STEPS:
        with st.expander(step,expanded=False):
            is_done[step]=st.checkbox("Mark step complete", value=is_done.get(step, False), key=f"done::{step}::{lead_id}")
with right:
    st.subheader("Case snapshot")
    with st.container(border=True):
        st.write(f"**Client:** {name}"); st.write(f"**City:** {city}"); st.write(f"**Status:** {str(status).replace('_',' ').title()}")
        st.write(f"**Assigned:** {assigned or '—'}"); st.write(f"**Budget:** "+(f"${int(budget):,}/mo" if isinstance(budget,(int,float)) and budget>0 else "—"))
        st.write(f"**Timeline:** {timeline or '—'}")
    st.caption("Quick note"); st.text_area(" ", key=f"intake_quick_note::{lead_id}", height=120, label_visibility="collapsed")
b1,b2=st.columns([1,1])
with b1:
    if st.button("Complete Intake → Start Placement", type="primary"):
        for k in INTAKE_STEPS: is_done[k]=True
        try:
            if hasattr(st,"switch_page"): st.switch_page("pages/91_Placement_Workflow.py")
        except Exception:
            st.session_state["_goto_page"]="pages/91_Placement_Workflow.py"; st.experimental_rerun()
with b2:
    st.button("← Back to Workflows", on_click=lambda: st.session_state.update({"_goto_page":"pages/89_Workflows.py"}))
