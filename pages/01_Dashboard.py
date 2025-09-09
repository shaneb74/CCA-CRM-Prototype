import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------- style ----------
st.markdown("""
<style>
.card {background:#fff;border:1px solid #e9edf3;border-radius:16px;padding:18px}
.kpi {display:flex;flex-direction:column;gap:8px}
.kpi h3 {margin:0;font-size:14px;color:#6b7280;font-weight:600}
.kpi .num {font-size:28px;font-weight:700;color:#111827;line-height:1}
.sub {font-size:12px;color:#6b7280}
.badge {display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;background:#eef2ff;color:#3730a3}
.badge.green {background:#ecfdf5;color:#065f46}
.badge.red {background:#fef2f2;color:#991b1b}
.badge.yellow {background:#fffbeb;color:#92400e}
.alert {background:#f7fbff;border:1px solid #e1f0ff;border-radius:12px;padding:10px 12px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center}
.alert .tag {font-size:11px;color:#2563eb;background:#eaf2ff;border-radius:999px;padding:2px 8px;margin-left:6px}
.kebab {border:none;background:transparent;color:#6b7280;cursor:pointer}
.section-title{font-weight:700;font-size:18px;margin:8px 0}
hr{border:none;border-top:1px solid #eef2f7;margin:8px 0 0}
</style>
""", unsafe_allow_html=True)

st.title("Advisor Dashboard")

# ---------- KPI row ----------
col1, col2, col3, col4 = st.columns([1,1,1,1.2])
with col1:
    st.markdown('<div class="card kpi"><h3>New leads (today)</h3><div class="num">5</div><div class="sub"><span class="badge green">+2 vs yesterday</span></div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card kpi"><h3>Assigned leads</h3><div class="num">12</div><div class="sub"><span class="badge green">+1 this week</span></div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card kpi"><h3>Active cases</h3><div class="num">3</div><div class="sub"><span class="badge red">-1 since Fri</span></div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="card kpi"><h3>MTD vs goal</h3><div class="num">$20,500 / $40,000</div><div class="sub"><span class="badge yellow">51% of goal</span></div></div>', unsafe_allow_html=True)

st.write("")

# ---------- Alerts ----------
st.markdown('<div class="section-title">Guidance & Alerts</div>', unsafe_allow_html=True)
alerts = [
    ("Upload signed Disclosure before scheduling tours.", "Compliance"),
    ("Confirm Medicaid rollover during financial review.", "Financial"),
    ("Keep intake notes date-stamped with initials.", "General"),
]
for msg, tag in alerts:
    c1, c2 = st.columns([10,1])
    with c1:
        st.markdown(f'<div class="alert">{msg} <span class="tag">{tag}</span></div>', unsafe_allow_html=True)
    with c2:
        st.button("✓", key=f"ack_{tag}")

# ---------- Tasks ----------
st.markdown('<div class="section-title">Tasks & Queues</div>', unsafe_allow_html=True)
left, right = st.columns(2)

due_today = [
    {"Task":"Call lead John Doe","Priority":"High","Due": datetime.now().date()},
    {"Task":"Prepare intake forms","Priority":"Med","Due": datetime.now().date()},
]
upcoming = [
    {"Task":"Follow up with client Jane","Priority":"Med","Due": datetime.now().date()+timedelta(days=1)},
    {"Task":"Schedule case review","Priority":"Low","Due": datetime.now().date()+timedelta(days=2)},
    {"Task":"Complete assessment for Mary Johnson","Priority":"High","Due": datetime.now().date()+timedelta(days=3)},
]

with left:
    st.markdown("**Due today**")
    df_today = pd.DataFrame(due_today)
    checked = st.experimental_data_editor(df_today, use_container_width=True, num_rows="dynamic", key="today_tbl")
with right:
    st.markdown("**Upcoming**")
    df_up = pd.DataFrame(upcoming)
    st.experimental_data_editor(df_up, use_container_width=True, num_rows="dynamic", key="up_tbl")

# Quick add
new = st.text_input("Add quick task")
if st.button("Add"):
    st.toast(f"Task added: {new}")

# ---------- Pipeline ----------
st.markdown('<div class="section-title">Pipeline by Workflow Stage</div>', unsafe_allow_html=True)
st.progress(0.51, text="Lead → Intake → Search → Decision → Transition → Invoice")

# ---------- Communications ----------
with st.expander("Communications"):
    st.write("Latest:")
    st.write("- VM from John Doe about tour availability")
    st.write("- Email to Mary J. with disclosure PDF")
    st.write("- SMS to Jane: confirmed Friday call")

# ---------- Workflows ----------
st.markdown('<div class="section-title">Advisor Workflows</div>', unsafe_allow_html=True)
with st.expander("Lead → Intake"):
    st.markdown("**Lead Received**  \nCall client and start intake (~30 min). Upload disclosure before tours.")
    st.markdown("**Client Intake**  \nComplete intake in CRM. Keep notes date-stamped.")
    st.button("Use as checklist", key="wf1")
with st.expander("Case Management → Search"):
    st.write("Qualify budget, location, care level. Shortlist 3 communities. Schedule tours.")
with st.expander("Decision → Transition → Invoice"):
    st.write("Confirm placement, transition checklist, send invoice and documentation.")