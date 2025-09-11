# 05_Supervisor_Workspace.py — adjusted to named advisors
import streamlit as st
from datetime import date
import store
from ui_chrome import apply_chrome
apply_chrome()  # idempotent

store.init()

st.title("Supervisor Workspace")

def _metrics_for(advisor_name: str):
    leads = [l for l in store.get_leads() if l.get("assigned_to") == advisor_name]
    active = [l for l in leads if l["status"] in ("new","in_progress")]
    tasks = []
    for t in store.get_tasks(True):
        lead = store.get_lead(t["lead_id"])
        if lead and lead.get("assigned_to") == advisor_name:
            tasks.append(t)
    due_today = sum(1 for t in tasks if t["due"] == date.today())
    overdue = sum(1 for t in tasks if t["due"] < date.today())
    return {"open_leads": len(leads), "active_cases": len(active), "tasks_due_today": due_today, "tasks_overdue": overdue}

advisors = store.ADVISORS[:6]  # show first 6
cards = [{"id": f"adv_{i}", "name": a, "m": _metrics_for(a)} for i, a in enumerate(advisors)]

selected_id = st.session_state.get("sup_selected_advisor", "adv_0")
st.session_state["sup_selected_advisor"] = selected_id

st.subheader("Team Overview")
rows = [st.columns(3), st.columns(3)]
idx = 0
for row in rows:
    for col in row:
        if idx >= len(cards): break
        card = cards[idx]
        with col:
            with st.container(border=True):
                st.markdown(f"**{card['name']}**")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Open leads", card["m"]["open_leads"])
                c2.metric("Active", card["m"]["active_cases"])
                c3.metric("Due today", card["m"]["tasks_due_today"])
                c4.metric("Overdue", card["m"]["tasks_overdue"])
                if st.button(("Selected" if card["id"] == selected_id else "View queue"), key=f"sel_{card['id']}", disabled=(card["id"] == selected_id)):
                    st.session_state["sup_selected_advisor"] = card["id"]
                    st.experimental_rerun()
        idx += 1

# Detail for selected advisor
sel_idx = int(st.session_state["sup_selected_advisor"].split("_")[1])
advisor_name = advisors[sel_idx]
st.subheader(f"{advisor_name} — Work Queue")

pairs = []
for t in store.get_tasks(True):
    lead = store.get_lead(t["lead_id"])
    if lead and lead.get("assigned_to") == advisor_name:
        pairs.append((t, lead))

left, right = st.columns(2)
with left:
    st.caption("Due today")
    for t, lead in [p for p in pairs if p[0]["due"] == date.today()]:
        with st.container(border=True):
            st.markdown(f"**{t['title']}**")
            st.caption(f"Lead: {lead['name']} • Due {t['due'].isoformat()}")
            if st.button("Mark complete", key=f"sup_done_{t['id']}"):
                store.complete_task(t["id"])
                st.experimental_rerun()

with right:
    st.caption("Upcoming")
    for t, lead in [p for p in pairs if p[0]["due"] > date.today()]:
        with st.container(border=True):
            st.markdown(f"**{t['title']}**")
            st.caption(f"Lead: {lead['name']} • Due {t['due'].isoformat()}")
            if st.button("Mark complete", key=f"sup_done_up_{t['id']}"):
                store.complete_task(t["id"])
                st.experimental_rerun()