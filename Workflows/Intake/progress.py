# Workflows/Intake/progress.py
import streamlit as st

MILESTONES = [
    ("lead_received", "Lead received"),
    ("lead_assigned", "Lead assigned"),
    ("initial_contact_attempted", "Initial contact attempted"),
    ("initial_contact_made", "Initial contact made"),
    ("consultation_scheduled", "Consultation scheduled"),
    ("assessment_started", "Assessment started"),
    ("assessment_completed", "Assessment completed"),
    ("qualified_decision", "Qualification decision"),
]

def _get_state(lead_id: str):
    st.session_state.setdefault('intake_status',{}).setdefault(lead_id,{})
    return st.session_state['intake_status'][lead_id]

def _pill_row(status: dict):
    done = [label for key,label in MILESTONES if status.get(key)]
    if not done:
        st.progress(0.05)
    else:
        pct = len(done) / len(MILESTONES)
        st.progress(pct)
    # badges
    for key,label in MILESTONES:
        color = "green" if status.get(key) else "gray"
        st.markdown(f"<span class='pill {color}'>{label}</span>", unsafe_allow_html=True)
    st.markdown("<div class='pill-spacer'></div>", unsafe_allow_html=True)

def ensure_css_spacing():
    css = '''
    <style>
      .pill {display:inline-block; font-size:12px; padding:4px 8px; margin-right:6px;
             border-radius:999px; background:#f3f4f6; color:#374151;}
      .pill.green { background:#d1fae5; color:#065f46; }
      .pill.gray { background:#f3f4f6; color:#6b7280; }
      .pill-spacer { height: 16px; }
      .exp-row { margin-bottom: 8px; }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

def show_intake_progress(lead_id: str):
    status = _get_state(lead_id)
    _pill_row(status)

    # expandable sections (content TBD)
    for key, label in MILESTONES:
        with st.expander(label, expanded=False):
            st.write("Tasks & notes coming soon.")