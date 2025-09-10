# 01_Dashboard.py — Dashboard with drawered Guidance & Alerts + badge for new items
import streamlit as st
from datetime import date, timedelta
import store
from ui_chrome import apply_chrome
apply_chrome()

# Safe init
store.init()

st.title("Advisor Dashboard")

# ------- lightweight styles
st.markdown(
    """
    <style>
      .page {max-width:1200px;margin:0 auto}
      .kpi .num {font-size:28px;font-weight:700;color:#111827}
      .badge {display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid rgba(0,0,0,0.06)}
      .badge.green {background:#ecfdf5;color:#065f46}
      .badge.yellow {background:#fffbeb;color:#92400e}
      .task-title{font-weight:600;color:#111827;margin-bottom:2px}
      .task-sub{font-size:12px;color:#6b7280}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="page">', unsafe_allow_html=True)

def kpi_card(title, value, sub_html=""):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(f"<div class='num'>{value}</div>", unsafe_allow_html=True)
        if sub_html:
            st.markdown(sub_html, unsafe_allow_html=True)

def badge(text, bg="#f3f4f6", fg="#374151"):
    st.markdown(
        f"<span class='badge' style='background:{bg};color:{fg}'> {text} </span>",
        unsafe_allow_html=True,
    )

# ======= KPIs
leads = store.get_leads()
leads_today = [x for x in leads if x["created"] == date.today()]
assigned = [x for x in leads if x["assigned_to"]]
active_cases = [x for x in leads if x["status"] in ("new", "in_progress")]

k1, k2, k3, k4 = st.columns([1, 1, 1, 1.2])
with k1:
    kpi_card("New leads (today)", len(leads_today), "<span class='badge green'>+2 vs yesterday</span>")
with k2:
    kpi_card("Assigned leads", len(assigned), "<span class='badge green'>+1 this week</span>")
with k3:
    kpi_card("Active cases", len(active_cases), "<span class='badge'>-1 since Fri</span>")
with k4:
    kpi_card("MTD vs goal", "$20,500 / $40,000", "<span class='badge yellow'>51% of goal</span>")

st.write("")

# ======= Guidance & Alerts (drawer with badge)
# keep alert state in session so the badge clears as items are acknowledged
if "guidance_alerts" not in st.session_state:
    st.session_state.guidance_alerts = [
        {"id": "A1", "tag": "Compliance", "msg": "Upload signed Disclosure before scheduling tours.", "acked": False},
        {"id": "A2", "tag": "Financial",  "msg": "Confirm Medicaid rollover during financial review.", "acked": False},
        {"id": "A3", "tag": "General",    "msg": "Keep intake notes date-stamped with initials.",      "acked": False},
    ]

alerts = st.session_state.guidance_alerts
new_count = sum(1 for a in alerts if not a.get("acked"))

drawer_label = f"Guidance & Alerts{'  🔔 ' + str(new_count) + ' new' if new_count else ''}"
exp = st.expander(drawer_label, expanded=False)

with exp:
    for a in alerts:
        with st.container(border=True):
            c1, c2 = st.columns([0.93, 0.07])
            with c1:
                st.write(a["msg"])
            with c2:
                st.markdown(f"<div style='text-align:right'>{a['tag']}</div>", unsafe_allow_html=True)
                if not a.get("acked"):
                    if st.button("✓", key=f"ack_{a['id']}"):
                        a["acked"] = True
                        st.experimental_rerun()
                else:
                    st.caption("Acked")

# Optional toast so the user doesn’t miss it when the drawer is closed
if new_count:
    st.toast(f"{new_count} new alert{'s' if new_count != 1 else ''}", icon="🔔")

# ======= Tasks & Queues
st.write("")
with st.expander("Tasks & Queues • Today: 2 • Upcoming: 3", expanded=True):
    left, right = st.columns(2)

    with left:
        st.caption("Due today")
        for t in [t for t in store.get_tasks(True) if t["due"] == date.today()]:
            with st.container(border=True):
                c_ac, c_main, c_btn = st.columns([0.05, 0.75, 0.20])
                with c_ac:
                    st.markdown(
                        "<div style='height:44px;width:6px;background:#d1d5db;border-radius:8px'></div>",
                        unsafe_allow_html=True,
                    )
                with c_main:
                    st.markdown(f"<div class='task-title'>{t['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='task-sub'>Due {t['due'].isoformat()}</div>", unsafe_allow_html=True)
                with c_btn:
                    if st.button("✓ Complete", key=f"done_dash_{t['id']}"):
                        store.complete_task(t["id"])
                        st.experimental_rerun()

        with st.form("quick_add_today_v4", clear_on_submit=True):
            st.caption("Add quick task")
            title = st.text_input("Task title", label_visibility="collapsed")
            prio = st.selectbox("Priority", ["High", "Med", "Low"], index=1, label_visibility="collapsed")
            submitted = st.form_submit_button("Add")
            if submitted and title:
                store.add_task(
                    {
                        "id": f"T-new-{len(store.get_tasks(False))+1}",
                        "title": title,
                        "lead_id": "LD-1001",
                        "priority": prio,
                        "due": date.today(),
                        "origin": "app",
                        "done": False,
                    }
                )
                st.experimental_rerun()

    with right:
        st.caption("Upcoming")
        for t in [t for t in store.get_tasks(True) if t["due"] > date.today()]:
            with st.container(border=True):
                c_ac, c_main, c_btn = st.columns([0.05, 0.75, 0.20])
                with c_ac:
                    st.markdown(
                        "<div style='height:44px;width:6px;background:#d1d5db;border-radius:8px'></div>",
                        unsafe_allow_html=True,
                    )
                with c_main:
                    st.markdown(f"<div class='task-title'>{t['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='task-sub'>Due {t['due'].isoformat()}</div>", unsafe_allow_html=True)
                with c_btn:
                    if st.button("✓ Complete", key=f"done_dash_up_{t['id']}"):
                        store.complete_task(t["id"])
                        st.experimental_rerun()

        with st.form("quick_add_up_v4", clear_on_submit=True):
            st.caption("Add task (upcoming)")
            title = st.text_input("Task title", label_visibility="collapsed", key="up_title")
            prio = st.selectbox("Priority", ["High", "Med", "Low"], index=2, key="up_prio", label_visibility="collapsed")
            due = st.date_input("Due date", value=date.today() + timedelta(days=1), key="up_due", label_visibility="collapsed")
            submitted = st.form_submit_button("Add")
            if submitted and title:
                store.add_task(
                    {
                        "id": f"T-new-{len(store.get_tasks(False))+1}",
                        "title": title,
                        "lead_id": "LD-1002",
                        "priority": prio,
                        "due": due,
                        "origin": "app",
                        "done": False,
                    }
                )
                st.experimental_rerun()

# ======= Pipeline
st.write("")
st.subheader("Pipeline by Workflow Stage")
st.caption("Lead ▸ Intake ▸ Search ▸ Decision ▸ Transition ▸ Invoice")
st.progress(0.62, text="Pipeline")

# ======= Communications
with st.expander("Communications", expanded=False):
    for who, msg in [
        ("You", "Left voicemail for John Doe."),
        ("John Doe", "Can we talk tomorrow after 2pm?"),
        ("You", "Confirmed intake on Thursday."),
    ]:
        with st.container(border=True):
            st.markdown(f"**{who}**")
            st.caption(msg)

# ======= Advisor Workflows
with st.expander("Advisor Workflows", expanded=False):
    for name in ["Lead ▸ Intake", "Case Management ▸ Search", "Decision ▸ Transition ▸ Invoice"]:
        with st.container(border=True):
            st.write(name)
            st.caption("Step-by-step checklist and guardrails.")

st.markdown("</div>", unsafe_allow_html=True)