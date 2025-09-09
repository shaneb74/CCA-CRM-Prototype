# 01_Dashboard.py — polished visuals + safe init
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

st.title("Advisor Dashboard")
st.markdown("""<style>\n  .page {max-width:1200px;margin:0 auto}\n  .card {background:#fff;border:1px solid #e9edf3;border-radius:16px;padding:18px}\n  .kpi h3 {margin:0;font-size:14px;color:#6b7280;font-weight:600}\n  .kpi .num {font-size:28px;font-weight:700;color:#111827;line-height:1}\n  .sub {font-size:12px;color:#6b7280}\n  .badge {display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid rgba(0,0,0,0.06)}\n  .badge.green {background:#ecfdf5;color:#065f46}\n  .badge.red {background:#fef2f2;color:#991b1b}\n  .badge.yellow {background:#fffbeb;color:#92400e}\n  .alert {background:#f7fbff;border:1px solid #e1f0ff;border-radius:12px;padding:10px 12px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center}\n  .alert .tag {font-size:11px;color:#2563eb;background:#eaf2ff;border-radius:999px;padding:2px 8px;margin-left:6px}\n  .section-title{font-weight:700;font-size:18px;margin:8px 0}\n  .task-title{font-weight:600;color:#111827;margin-bottom:2px}\n  .task-sub{font-size:12px;color:#6b7280}\n  .overdue{color:#b91c1c !important}\n</style>""", unsafe_allow_html=True)
st.markdown('<div class="page">', unsafe_allow_html=True)
leads = store.get_leads()
leads_today = [x for x in leads if x["created"] == date.today()]
assigned = [x for x in leads if x["assigned_to"]]
active_cases = [x for x in leads if x["status"] in ("new","in_progress")]
k1, k2, k3, k4 = st.columns([1,1,1,1.2])
with k1: kpi_card("New leads (today)", len(leads_today), '<span class="badge green">+ App and other sources</span>')
with k2: kpi_card("Assigned leads", len(assigned))
with k3: kpi_card("Active cases", len(active_cases))
with k4: kpi_card("MTD vs goal", "$20,500 / $40,000", '<span class="badge yellow">51% of goal</span>')
st.write("")
st.markdown('<div class="section-title">New Leads (Today)</div>', unsafe_allow_html=True)
if not leads_today:
    st.write("No new leads today.")
else:
    for lead in leads_today[:6]:
        c1, c2, c3, c4, c5 = st.columns([0.35, 0.15, 0.20, 0.20, 0.10])
        with c1:
            st.markdown(f"**{{lead['name']}}**")
            st.caption(lead["city"])
        with c2:
            if lead["origin"] == "app":
                badge("App Lead", "#ecfdf5", "#065f46")
            elif lead["origin"] == "phone":
                badge("Phone", "#eff6ff", "#1d4ed8")
            else:
                badge(lead["origin"].title())
        with c3:
            st.caption((lead["preference"] + (f" — est. ${{lead['budget']:,}}" if lead["budget"] else "")))
        with c4:
            st.caption(f"Timeline: {{lead['timeline']}}")
        with c5:
            if st.button("Open", key=f"open_{{lead['id']}}"):
                store.set_selected_lead(lead["id"])
                if hasattr(st, "switch_page"):
                    st.switch_page("pages/04_Client_Record.py")
                else:
                    st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)
