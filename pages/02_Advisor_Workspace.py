# 02_Advisor_Workspace.py — Work Queue with attractive cards
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

st.title("Advisor Workspace")
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
left, right = st.columns([0.7, 0.3])
with left:
    origin = segmented("Origin", ["All","App","Phone","Hospital"], "All")
with right:
    due_filter = segmented("Due", ["All","Today","Upcoming"], "All")
def origin_match(o):
    if origin == "All": return True
    return o == {"App":"app","Phone":"phone","Hospital":"hospital"}[origin]
def due_match(d):
    if due_filter == "All": return True
    if due_filter == "Today": return d == date.today()
    return d > date.today()
tasks = [t for t in store.get_tasks(True) if origin_match(t["origin"]) and due_match(t["due"])]
leads = {l["id"]: l for l in store.get_leads()}
if not tasks:
    st.info("Nothing in your queue.")
else:
    for t in tasks:
        lead = leads.get(t["lead_id"])
        with st.container(border=True):
            c_accent, c_main, c_chip, c_btn = st.columns([0.03, 0.62, 0.17, 0.18])
            overdue = t["due"] < date.today()
            accent = "#dc2626" if (t["priority"] == "High" and overdue) else ("#f59e0b" if t["priority"] == "Med" and overdue else "#d1d5db")
            with c_accent:
                st.markdown(f"<div style='width:6px;height:54px;background:{accent};border-radius:10px;'></div>", unsafe_allow_html=True)
            with c_main:
                st.markdown(f"<div class='task-title'>{t['title']}</div>", unsafe_allow_html=True)
                sub = f"Due {t['due'].isoformat()}"
                if lead:
                    sub = lead['name'] + " • " + lead['city'] + "  ·  " + sub
                st.markdown(f"<div class='task-sub'>{sub}</div>", unsafe_allow_html=True)
            with c_chip:
                if t["origin"] == "app":
                    badge("App Lead", "#ecfdf5", "#065f46")
                else:
                    badge(t["origin"].title())
            with c_btn:
                cb1, cb2 = st.columns([0.6,0.4])
                with cb1:
                    if st.button("Open", key=f"open_task_{t['id']}"):
                        store.set_selected_lead(t["lead_id"])
                        if hasattr(st, "switch_page"):
                            st.switch_page("pages/04_Client_Record.py")
                        else:
                            st.experimental_rerun()
                with cb2:
                    if st.button("✓", key=f"done_{t['id']}", help="Complete"):
                        store.complete_task(t["id"])
                        st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)
