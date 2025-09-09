# 01_Dashboard.py — stable dashboard; Streamlit-safe task rows (no stray frames)

import streamlit as st
from datetime import date, timedelta

# ---------- App/page config ----------
st.set_page_config(
    page_title="Advisor Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Minimal CSS ----------
def inject_css():
    st.markdown("""
    <style>
      .page {max-width:1200px;margin:0 auto}
      .card {background:#fff;border:1px solid #e9edf3;border-radius:16px;padding:18px}
      .kpi {display:flex;flex-direction:column;gap:8px}
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
      .btn-plain {background:#f3f4f6;border:1px solid #d1d5db;border-radius:8px;padding:6px 10px;font-size:13px}
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ---------- Helpers ----------
def kpi_card(title, value, sub_html=""):
    st.markdown(
        f'<div class="card kpi"><h3>{title}</h3><div class="num">{value}</div>'
        f'<div class="sub">{sub_html}</div></div>', unsafe_allow_html=True
    )

def alert_row(message, tag, key):
    c1, c2 = st.columns([10,1])
    with c1:
        st.markdown(f'<div class="alert">{message} <span class="tag">{tag}</span></div>',
                    unsafe_allow_html=True)
    with c2:
        st.button("✓", key=f"ack_{key}")

PRIORITY = {
    "High": {"accent": "#dc2626", "chip_bg": "#fee2e2", "chip_fg": "#991b1b"},
    "Med":  {"accent": "#f59e0b", "chip_bg": "#fef9c3", "chip_fg": "#92400e"},
    "Low":  {"accent": "#9ca3af", "chip_bg": "#e5e7eb", "chip_fg": "#374151"},
}

def accent_color(task):
    return PRIORITY.get(task["priority"], PRIORITY["Low"])["accent"] if task["due"] < date.today() else "#d1d5db"

def task_card(task, key_prefix, list_name):
    """Streamlit-only layout: left accent col + bordered card with real widgets."""
    # Row container
    row = st.container()
    with row:
        # Narrow accent + main card
        ac, body = st.columns([0.02, 0.98])
        # Accent bar (fixed height to match content)
        with ac:
            st.markdown(
                f"<div style='width:6px;height:54px;background:{accent_color(task)};border-radius:10px;'></div>",
                unsafe_allow_html=True,
            )
        with body:
            # Bordered card with content columns
            with st.container(border=True):
                c1, c2, c3 = st.columns([0.64, 0.18, 0.18])
                with c1:
                    overdue = task["due"] < date.today()
                    due_cls = "task-sub overdue" if overdue else "task-sub"
                    st.markdown(f"<div class='task-title'>{task['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='{due_cls}'>Due {task['due'].isoformat()}</div>", unsafe_allow_html=True)
                with c2:
                    chip = PRIORITY.get(task["priority"], PRIORITY["Low"])
                    st.markdown(
                        f"<span class='badge' style='background:{chip['chip_bg']};color:{chip['chip_fg']}'>{task['priority']}</span>",
                        unsafe_allow_html=True,
                    )
                with c3:
                    if st.button("✓ Complete", key=f"{key_prefix}_{task['title']}"):
                        st.session_state[list_name] = [t for t in st.session_state[list_name] if t is not task]
                        st.experimental_rerun()

def count_overdue(tasks):
    return sum(1 for t in tasks if t["due"] < date.today())

# ---------- Seed demo state ----------
if "tasks_today" not in st.session_state:
    st.session_state.tasks_today = [
        {"title":"Call lead John Doe","priority":"High","due":date.today()},
        {"title":"Prepare intake forms","priority":"Med","due":date.today()},
    ]
if "tasks_upcoming" not in st.session_state:
    st.session_state.tasks_upcoming = [
        {"title":"Follow up with client Jane","priority":"Med","due":date.today()+timedelta(days=1)},
        {"title":"Schedule case review","priority":"Low","due":date.today()+timedelta(days=2)},
        {"title":"Complete assessment for Mary Johnson","priority":"High","due":date.today()+timedelta(days=3)},
    ]

# ---------- Page ----------
with st.container():
    st.title("Advisor Dashboard")
    st.markdown('<div class="page">', unsafe_allow_html=True)

    # KPI row
    k1, k2, k3, k4 = st.columns([1,1,1,1.2])
    with k1: kpi_card("New leads (today)", "5", '<span class="badge green">+2 vs yesterday</span>')
    with k2: kpi_card("Assigned leads", "12", '<span class="badge green">+1 this week</span>')
    with k3: kpi_card("Active cases", "3", '<span class="badge red">-1 since Fri</span>')
    with k4: kpi_card("MTD vs goal", "$20,500 / $40,000", '<span class="badge yellow">51% of goal</span>')

    st.write("")

    # Alerts
    st.markdown('<div class="section-title">Guidance & Alerts</div>', unsafe_allow_html=True)
    alert_row("Upload signed Disclosure before scheduling tours.", "Compliance", "disclosure")
    alert_row("Confirm Medicaid rollover during financial review.", "Financial", "medicaid")
    alert_row("Keep intake notes date-stamped with initials.", "General", "notes")

    # --------- Tasks & Queues (collapsible drawer) ----------
    today_cnt    = len(st.session_state.get("tasks_today", []))
    upcoming_cnt = len(st.session_state.get("tasks_upcoming", []))
    overdue_cnt  = count_overdue(st.session_state.get("tasks_today", [])) + count_overdue(st.session_state.get("tasks_upcoming", []))
    header = f"Tasks & Queues  •  Today: {today_cnt}  •  Upcoming: {upcoming_cnt}" + (f"  •  Overdue: {overdue_cnt}" if overdue_cnt else "")

    with st.expander(header, expanded=True):
        left, right = st.columns(2)

        # Today
        with left:
            st.markdown("**Due today**")
            prio_rank = {"High":0, "Med":1, "Low":2}
            for i, t in enumerate(sorted(st.session_state.tasks_today,
                                         key=lambda x: (prio_rank.get(x['priority'], 9), x['title']))):
                task_card(t, f"today_{i}", "tasks_today")

            # Quick add (today)
            with st.form("quick_add_today", clear_on_submit=True):
                nt = st.text_input("Add quick task", placeholder="Task title")
                np = st.selectbox("Priority", ["High","Med","Low"], index=1)
                submitted = st.form_submit_button("Add")
                if submitted and nt.strip():
                    st.session_state.tasks_today.append({"title": nt.strip(), "priority": np, "due": date.today()})
                    st.experimental_rerun()

        # Upcoming
        with right:
            st.markdown("**Upcoming**")
            for i, t in enumerate(sorted(st.session_state.tasks_upcoming, key=lambda x: (x["due"], x["title"]))):
                task_card(t, f"up_{i}", "tasks_upcoming")

            # Add to upcoming
            with st.form("quick_add_upcoming", clear_on_submit=True):
                nt2 = st.text_input("Add task (upcoming)", placeholder="Task title")
                np2 = st.selectbox("Priority ", ["High","Med","Low"], index=2, key="prio2")
                dd2 = st.date_input("Due date", value=date.today()+timedelta(days=1), min_value=date.today())
                sub2 = st.form_submit_button("Add")
                if sub2 and nt2.strip():
                    st.session_state.tasks_upcoming.append({"title": nt2.strip(), "priority": np2, "due": dd2})
                    st.experimental_rerun()

    # Pipeline
    st.markdown('<div class="section-title">Pipeline by Workflow Stage</div>', unsafe_allow_html=True)
    st.progress(0.51, text="Lead → Intake → Search → Decision → Transition → Invoice")

    # Communications
    with st.expander("Communications"):
        st.write("- VM from John Doe about tour availability")
        st.write("- Email to Mary J. with disclosure PDF")
        st.write("- SMS to Jane: confirmed Friday call")

    # Workflows
    st.markdown('<div class="section-title">Advisor Workflows</div>', unsafe_allow_html=True)
    with st.expander("Lead → Intake"):
        st.markdown("**Lead Received**  \nCall client and start intake (~30 min). Upload disclosure before tours.")
        st.markdown("**Client Intake**  \nComplete intake in CRM. Keep notes date-stamped.")
        st.button("Use as checklist", key="wf1")
    with st.expander("Case Management → Search"):
        st.write("Qualify budget, location, care level. Shortlist 3 communities. Schedule tours.")
    with st.expander("Decision → Transition → Invoice"):
        st.write("Confirm placement, transition checklist, send invoice and documentation.")

    st.markdown('</div>', unsafe_allow_html=True)