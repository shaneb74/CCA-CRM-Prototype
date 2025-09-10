# 03_Notifications.py — prettier alerts
import streamlit as st, store
from datetime import date, timedelta
from ui_chrome import apply_chrome
apply_chrome()

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

st.title("Notifications")
st.markdown("""<style>
  .page {max-width:1200px;margin:0 auto}
  .card {background:#fff;border:1px solid #e9edf3;border-radius:16px;padding:18px}
  .kpi h3 {margin:0;font-size:14px;color:#6b7280;font-weight:600}
  .kpi .num {font-size:28px;font-weight:700;color:#111827;line-height:1}
  .sub {font-size:12px;color:#6b7280}
  .badge {display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid rgba(0,0,0,0.06)}
  .badge.green {background:#ecfdf5;color:#065f46}
  .badge.red {background:#fef2f2;color:#991b1b}
  .badge.yellow {background:#fffbeb;color:#92400e}
  .alert {background:#f7fbff;border:1px solid #e1f0ff;border-radius:12px;padding:10px 12px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center}
  .alert .tag {font-size:11px;color:#2563eb;background:#eaf2ff;border-radius:999px;padding:2px 8px;margin-left:6px}
  .section-title{font-weight:700;font-size:18px;margin:8px 0}
  .task-title{font-weight:600;color:#111827;margin-bottom:2px}
  .task-sub{font-size:12px;color:#6b7280}
  .overdue{color:#b91c1c !important}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="page">', unsafe_allow_html=True)
alerts = [
    ("Compliance", "Upload signed Disclosure before scheduling tours."),
    ("Financial", "Confirm Medicaid rollover during financial review."),
    ("General", "Keep intake notes date-stamped with initials."),
]
for idx, (tag, msg) in enumerate(alerts, start=1):
    c1, c2 = st.columns([0.92, 0.08])
    with c1:
        st.markdown(f"<div class='alert'>{msg} <span class='tag'>{tag}</span></div>", unsafe_allow_html=True)
    with c2:
        st.button("✓", key=f"ack_{idx}")
st.markdown('</div>', unsafe_allow_html=True)
