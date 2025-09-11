# pages/90_Intake_Workflow.py — Intake Workflow (horizontal tracker + compact summary)
from __future__ import annotations
import streamlit as st

try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    pass

import store

st.set_page_config(page_title="Intake Workflow", page_icon="🧭", layout="wide")
store.init()

lead_id = store.get_selected_lead_id()
if not lead_id:
    st.info("No client selected. Use Client Record or the Workflows hub.")
    st.stop()

lead = store.get_lead(lead_id) or {}
name = lead.get("name","—")
city = lead.get("city","—")
status = str(lead.get("status","")).replace("_"," ")
budget = lead.get("budget")
timeline = lead.get("timeline","—")
notes = lead.get("notes","").strip()

st.title("Intake Workflow")
# --- Compact case summary row (matches your typography scale) ---
hc1, hc2, hc3, hc4 = st.columns([2,1,1,2])
with hc1:
    st.markdown(f"**{name} • {city}**")
with hc2:
    st.caption("Status")
    st.write(status or "—")
with hc3:
    st.caption("Budget / mo")
    st.write(f"{int(budget):,}" if isinstance(budget,(int,float)) and budget else "—")
with hc4:
    st.caption("Timeline")
    st.write(timeline or "—")

# --- Steps model (8 stages) ---
STEPS = [
    "Lead received",
    "Lead assigned",
    "Initial contact attempted",
    "Initial contact made",
    "Consultation scheduled",
    "Assessment started",
    "Assessment completed",
    "Qualification decision",
]

# Persist check states per lead across runs
def _step_key(i:int)->str:
    return f"intake_{lead_id}_{i}"

# Compute counts from current session_state
done_count = sum(1 for i in range(len(STEPS)) if st.session_state.get(_step_key(i), False))
progress = 0.0 if len(STEPS)==0 else min(1.0, done_count/len(STEPS))
current_idx = min(done_count, len(STEPS)-1)

# --- Horizontal pills (CSS) + progress bar ---
st.markdown('''
<style>
.cca-pillrow { display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:8px; margin: 6px 0 12px 0; }
.cca-pill {
  border-radius: 999px; padding: 6px 10px; font-size: 12px;
  border: 1px solid #e5e7eb; color:#6b7280; text-align:center; background:#fff;
  white-space: nowrap; overflow:hidden; text-overflow: ellipsis;
}
.cca-pill.done { background:#eef6ff; color:#2563eb; border-color:#bfdbfe; font-weight:600; }
.cca-pill.curr { border-color:#60a5fa; box-shadow: 0 0 0 2px rgba(59,130,246,0.15) inset; color:#1f2937; font-weight:600; }
</style>
''', unsafe_allow_html=True)

st.caption("Intake progress")
progress_bar = st.progress(progress)

# Pill row
pill_html = '<div class="cca-pillrow">'
for i, label in enumerate(STEPS):
    cls = "cca-pill"
    if i < done_count:
        cls += " done"
    elif i == current_idx:
        cls += " curr"
    pill_html += f'<div class="{cls}">{label}</div>'
pill_html += "</div>"
st.markdown(pill_html, unsafe_allow_html=True)

# --- Expanders (kept, but slimmer spacing) ---
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

def _expander(label:str, idx:int):
    with st.expander(label, expanded=False):
        st.checkbox("Mark step complete", key=_step_key(idx))
        st.text_area("Notes", key=f"notes_{lead_id}_{idx}", height=80, placeholder="Add details…")

# Render grouped expanders
for i, label in enumerate(STEPS):
    _expander(label, i)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# --- Footer CTAs ---
def _go_back():
    st.session_state["_goto_page"] = "pages/89_Workflows.py"
    try:
        if hasattr(st, "switch_page"):
            st.switch_page("pages/89_Workflows.py")
    except Exception:
        pass

def _complete_and_go():
    # Mark all steps complete if user explicitly completes intake
    for i in range(len(STEPS)):
        st.session_state[_step_key(i)] = True
    st.session_state["_goto_page"] = "pages/91_Placement_Workflow.py"
    try:
        if hasattr(st, "switch_page"):
            st.switch_page("pages/91_Placement_Workflow.py")
    except Exception:
        pass

cta1, cta2 = st.columns([1,3])
with cta1:
    st.button("Complete Intake → Start Placement", type="primary", on_click=_complete_and_go)
with cta2:
    st.button("← Back to Workflows", on_click=_go_back)
