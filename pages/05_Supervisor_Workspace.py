# 05_Supervisor_Workspace.py — Supervisor view (6 advisors; Advisor A wired to live data)
import streamlit as st
from datetime import date
import store

store.init()

st.title("Supervisor Workspace")

# ---------------- Styles
st.markdown(
    """
    <style>
      .page {max-width:1200px;margin:0 auto}
      .tile h4 {margin: 0 0 6px 0}
      .k {font-size:12px;color:#6b7280}
      .v {font-weight:600}
      .chip {display:inline-block;padding:2px 8px;border:1px solid #e5e7eb;border-radius:999px;font-size:12px;margin-left:8px}
      .task-title{font-weight:600;color:#111827;margin-bottom:2px}
      .task-sub{font-size:12px;color:#6b7280}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="page">', unsafe_allow_html=True)

# ---------------- Helpers
def _live_metrics_for(name: str):
    leads = [l for l in store.get_leads() if l.get("assigned_to") == name]
    active_cases = [l for l in leads if l["status"] in ("new", "in_progress")]
    tasks = []
    for t in store.get_tasks(True):
        lead = store.get_lead(t["lead_id"])
        if lead and lead.get("assigned_to") == name:
            tasks.append(t)
    due_today = sum(1 for t in tasks if t["due"] == date.today())
    overdue = sum(1 for t in tasks if t["due"] < date.today())
    return {
        "open_leads": len(leads),
        "active_cases": len(active_cases),
        "tasks_due_today": due_today,
        "tasks_overdue": overdue,
    }

def _render_tile(ad, selected: bool):
    with st.container(border=True):
        st.markdown(f"<div class='tile'><h4>{ad['name']}</h4></div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='k'>Open leads</div><div class='v'>{ad['m']['open_leads']}</div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='k'>Active cases</div><div class='v'>{ad['m']['active_cases']}</div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='k'>Due today</div><div class='v'>{ad['m']['tasks_due_today']}</div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='k'>Overdue</div><div class='v'>{ad['m']['tasks_overdue']}</div>", unsafe_allow_html=True)
        st.caption(" ")
        label = "Selected" if selected else "View queue"
        disabled = selected
        if st.button(label, key=f"sel_{ad['id']}", disabled=disabled):
            st.session_state["sup_selected_advisor"] = ad["id"]
            st.experimental_rerun()

# ---------------- Data
# One “real” advisor using store; others mocked for demo
advisors = [
    {"id": "adv_a", "name": "Advisor A", "m": _live_metrics_for("Advisor A")},
    {"id": "adv_b", "name": "Advisor B", "m": {"open_leads": 3, "active_cases": 2, "tasks_due_today": 1, "tasks_overdue": 0}},
    {"id": "adv_c", "name": "Advisor C", "m": {"open_leads": 7, "active_cases": 4, "tasks_due_today": 2, "tasks_overdue": 1}},
    {"id": "adv_d", "name": "Advisor D", "m": {"open_leads": 1, "active_cases": 1, "tasks_due_today": 0, "tasks_overdue": 0}},
    {"id": "adv_e", "name": "Advisor E", "m": {"open_leads": 5, "active_cases": 3, "tasks_due_today": 1, "tasks_overdue": 2}},
    {"id": "adv_f", "name": "Advisor F", "m": {"open_leads": 4, "active_cases": 2, "tasks_due_today": 0, "tasks_overdue": 1}},
]

selected_id = st.session_state.get("sup_selected_advisor", "adv_a")
st.session_state["sup_selected_advisor"] = selected_id

# ---------------- Overview grid (3 x 2)
st.subheader("Team Overview")
row1 = st.columns(3)
for i, col in enumerate(row1):
    with col:
        _render_tile(advisors[i], selected=(advisors[i]["id"] == selected_id))

row2 = st.columns(3)
for i, col in enumerate(row2):
    with col:
        _render_tile(advisors[i + 3], selected=(advisors[i + 3]["id"] == selected_id))

# ---------------- Detail panel for selected advisor
sel = next(a for a in advisors if a["id"] == selected_id)
st.write("")
st.subheader(f"{sel['name']} — Work Queue")

def _tasks_for_advisor(name: str):
    out = []
    for t in store.get_tasks(True):
        lead = store.get_lead(t["lead_id"])
        if lead and lead.get("assigned_to") == name:
            out.append((t, lead))
    return out

# live only for Advisor A; others use a static mock list
if sel["id"] == "adv_a":
    pairs = _tasks_for_advisor("Advisor A")
else:
    # fake 3 tasks for demo advisors
    pairs = [
        ({"id":"DEMO-1","title":"Call intake follow-up","lead_id":"LD-X1","priority":"Med","due":date.today(),"origin":"app"}, {"id":"LD-X1","name":"Demo Lead 1","city":"N/A"}),
        ({"id":"DEMO-2","title":"Schedule RN assessment","lead_id":"LD-X2","priority":"High","due":date.today(),"origin":"phone"}, {"id":"LD-X2","name":"Demo Lead 2","city":"N/A"}),
        ({"id":"DEMO-3","title":"Send disclosure packet","lead_id":"LD-X3","priority":"Low","due":date.today(),"origin":"hospital"}, {"id":"LD-X3","name":"Demo Lead 3","city":"N/A"}),
    ]

left, right = st.columns(2)

with left:
    st.caption("Due today")
    for t, lead in [p for p in pairs if p[0]["due"] == date.today()]:
        with st.container(border=True):
            st.markdown(f"<div class='task-title'>{t['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='task-sub'>Lead: {lead['name']} • Due {t['due'].isoformat()}</div>", unsafe_allow_html=True)
            c1, c2 = st.columns([0.5, 0.5])
            with c1:
                if st.button("Mark complete", key=f"sup_done_{sel['id']}_{t['id']}"):
                    store.complete_task(t["id"])
                    st.experimental_rerun()
            with c2:
                if st.button("Client Record", key=f"sup_open_{sel['id']}_{t['id']}"):
                    # navigate to full record if possible
                    store.set_selected_lead(lead["id"])
                    if hasattr(st, "switch_page"):
                        st.switch_page("pages/04_Client_Record.py")
                    else:
                        st.experimental_rerun()

with right:
    st.caption("Upcoming")
    for t, lead in [p for p in pairs if p[0]["due"] > date.today()]:
        with st.container(border=True):
            st.markdown(f"<div class='task-title'>{t['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='task-sub'>Lead: {lead['name']} • Due {t['due'].isoformat()}</div>", unsafe_allow_html=True)
            c1, c2 = st.columns([0.5, 0.5])
            with c1:
                if st.button("Mark complete", key=f"sup_done_up_{sel['id']}_{t['id']}"):
                    store.complete_task(t["id"])
                    st.experimental_rerun()
            with c2:
                if st.button("Client Record", key=f"sup_open_up_{sel['id']}_{t['id']}"):
                    store.set_selected_lead(lead["id"])
                    if hasattr(st, "switch_page"):
                        st.switch_page("pages/04_Client_Record.py")
                    else:
                        st.experimental_rerun()

# Quick KPIs for the selected advisor
st.write("")
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open leads", sel["m"]["open_leads"])
    c2.metric("Active cases", sel["m"]["active_cases"])
    c3.metric("Tasks due today", sel["m"]["tasks_due_today"])
    c4.metric("Overdue tasks", sel["m"]["tasks_overdue"])

st.markdown('</div>', unsafe_allow_html=True)