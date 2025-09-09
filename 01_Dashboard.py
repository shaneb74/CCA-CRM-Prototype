# 01_Dashboard.py — restored full dashboard layout
import streamlit as st, store
from datetime import date, timedelta
store.init()

def segmented(label, options, default):
    if hasattr(st, "segmented_control"):
        return st.segmented_control(label, options=options, default=default)
    return st.radio(label, options, index=options.index(default), horizontal=True)

def badge(text, bg="#f3f4f6", fg="#374151"):
    st.markdown(f"<span class='badge' style='background:{bg};color:{fg}'> {text} </span>", unsafe_allow_html=True)

def kpi_card(title, value, sub_html=""):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(f"<div class='num'>{value}</div>", unsafe_allow_html=True)
        if sub_html:
            st.markdown(sub_html, unsafe_allow_html=True)


st.title("Advisor Dashboard")
st.markdown("""<style>
  .page {max-width:1200px;margin:0 auto}
  .kpi .num {font-size:28px;font-weight:700;color:#111827}
  .badge {display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid rgba(0,0,0,0.06)}
  .badge.green {background:#ecfdf5;color:#065f46}
  .badge.yellow {background:#fffbeb;color:#92400e}
  .rowcard {border:1px solid #e5e7eb;border-radius:14px;padding:12px;background:#fff}
  .task-title{font-weight:600;color:#111827;margin-bottom:2px}
  .task-sub{font-size:12px;color:#6b7280}
  .lead-card{border:1px solid #e5e7eb;border-radius:14px;padding:12px;background:#fff}
  .lead-card:hover{box-shadow:0 0 0 2px #e5e7eb}
  .summary-card{border:1px solid #e5e7eb;border-radius:14px;padding:16px;background:#fff}
  .dim{color:#6b7280}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="page">', unsafe_allow_html=True)

from datetime import date

leads = store.get_leads()
leads_today = [x for x in leads if x["created"] == date.today()]
assigned = [x for x in leads if x["assigned_to"]]
active_cases = [x for x in leads if x["status"] in ("new","in_progress")]

k1, k2, k3, k4 = st.columns([1,1,1,1.2])
with k1: kpi_card("New leads (today)", len(leads_today), "<span class='badge green'>+2 vs yesterday</span>")
with k2: kpi_card("Assigned leads", len(assigned), "<span class='badge green'>+1 this week</span>")
with k3: kpi_card("Active cases", len(active_cases), "<span class='badge'>-1 since Fri</span>")
with k4: kpi_card("MTD vs goal", "$20,500 / $40,000", "<span class='badge yellow'>51% of goal</span>")

# Guidance & Alerts
st.write("")
st.subheader("Guidance & Alerts")
for tag, msg in [("Compliance","Upload signed Disclosure before scheduling tours."),
                 ("Financial","Confirm Medicaid rollover during financial review."),
                 ("General","Keep intake notes date-stamped with initials.")]:
    with st.container(border=True):
        c1, c2 = st.columns([0.93, 0.07])
        with c1: st.write(msg)
        with c2:
            st.markdown(f"<div style='text-align:right'>{tag}</div>", unsafe_allow_html=True)
            st.button("✓", key=f"ack_dash_{tag}")

st.write("")
with st.expander("Tasks & Queues • Today: 2 • Upcoming: 3", expanded=True):
    left, right = st.columns(2)
    with left:
        st.caption("Due today")
        for t in [t for t in store.get_tasks(True) if t["due"] == date.today()]:
            with st.container(border=True):
                c_ac, c_main, c_btn = st.columns([0.05, 0.75, 0.20])
                with c_ac: st.markdown("<div style='height:44px;width:6px;background:#d1d5db;border-radius:8px'></div>", unsafe_allow_html=True)
                with c_main:
                    st.markdown(f"<div class='task-title'>{t['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='task-sub'>Due {t['due'].isoformat()}</div>", unsafe_allow_html=True)
                with c_btn:
                    st.button("✓ Complete", key=f"done_dash_{t['id']}")
        # quick add
        with st.form("quick_add_today_v4", clear_on_submit=True):
            st.caption("Add quick task")
            title = st.text_input("Task title", label_visibility="collapsed")
            prio = st.selectbox("Priority", ["High","Med","Low"], index=1, label_visibility="collapsed")
            submitted = st.form_submit_button("Add")
            if submitted and title:
                from datetime import date
                store.add_task({"id": f"T-new-{len(store.get_tasks(False))+1}", "title": title, "lead_id": "LD-1001", "priority": prio, "due": date.today(), "origin":"app", "done": False})
                st.experimental_rerun()
    with right:
        st.caption("Upcoming")
        for t in [t for t in store.get_tasks(True) if t["due"] > date.today()]:
            with st.container(border=True):
                c_ac, c_main, c_btn = st.columns([0.05, 0.75, 0.20])
                with c_ac: st.markdown("<div style='height:44px;width:6px;background:#d1d5db;border-radius:8px'></div>", unsafe_allow_html=True)
                with c_main:
                    st.markdown(f"<div class='task-title'>{t['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='task-sub'>Due {t['due'].isoformat()}</div>", unsafe_allow_html=True)
                with c_btn:
                    st.button("✓ Complete", key=f"done_dash_up_{t['id']}")
        with st.form("quick_add_up_v4", clear_on_submit=True):
            st.caption("Add task (upcoming)")
            title = st.text_input("Task title", label_visibility="collapsed", key="up_title")
            prio = st.selectbox("Priority", ["High","Med","Low"], index=2, key="up_prio", label_visibility="collapsed")
            due = st.date_input("Due date", value=date.today()+timedelta(days=1), key="up_due", label_visibility="collapsed")
            submitted = st.form_submit_button("Add")
            if submitted and title:
                store.add_task({"id": f"T-new-{len(store.get_tasks(False))+1}", "title": title, "lead_id": "LD-1002", "priority": prio, "due": due, "origin":"app", "done": False})
                st.experimental_rerun()

st.write("")
st.subheader("Pipeline by Workflow Stage")
st.caption("Lead ▸ Intake ▸ Search ▸ Decision ▸ Transition ▸ Invoice")
st.progress(0.62, text="Pipeline")

with st.expander("Communications", expanded=False):
    for i, (who, msg) in enumerate([("You","Left voicemail for John Doe."),
                                    ("John Doe","Can we talk tomorrow after 2pm?"),
                                    ("You","Confirmed intake on Thursday.")], start=1):
        with st.container(border=True):
            st.markdown(f"**{who}**")
            st.caption(msg)

with st.expander("Advisor Workflows", expanded=False):
    for name in ["Lead ▸ Intake", "Case Management ▸ Search", "Decision ▸ Transition ▸ Invoice"]:
        with st.container(border=True):
            st.write(name)
            st.caption("Step-by-step checklist and guardrails.")

st.markdown('</div>', unsafe_allow_html=True)
