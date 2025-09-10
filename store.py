from datetime import date, timedelta
import streamlit as st

def init():
    if "leads" not in st.session_state:
        st.session_state.leads = _seed_leads()
    if "tasks" not in st.session_state:
        st.session_state.tasks = _seed_tasks()
    st.session_state.setdefault("selected_lead_id", None)

def get_leads():
    return st.session_state.leads

def get_lead(lead_id: str):
    return next((x for x in st.session_state.leads if x["id"] == lead_id), None)

def upsert_lead(updated: dict):
    for i, l in enumerate(st.session_state.leads):
        if l["id"] == updated["id"]:
            st.session_state.leads[i] = updated
            return
    st.session_state.leads.append(updated)

# ---- Progress helpers ----
def get_progress(lead_id: str) -> float:
    lead = get_lead(lead_id)
    return float(lead.get("progress", 0.0)) if lead else 0.0

def set_progress(lead_id: str, value: float):
    value = max(0.0, min(1.0, float(value)))
    lead = get_lead(lead_id)
    if lead:
        lead["progress"] = value
        upsert_lead(lead)

def get_tasks(active_only=True):
    tasks = st.session_state.tasks
    return [t for t in tasks if not t.get("done")] if active_only else tasks

def complete_task(task_id: str):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["done"] = True
            break

def add_task(task: dict):
    st.session_state.tasks.append(task)

def set_selected_lead(lead_id: str | None):
    st.session_state.selected_lead_id = lead_id

def get_selected_lead_id():
    return st.session_state.selected_lead_id

def _seed_leads():
    return [
        {
            "id": "LD-1001",
            "name": "John Doe",
            "origin": "app",
            "city": "Baton Rouge",
            "preference": "Assisted Living",
            "budget": 4500,
            "timeline": "30 days",
            "notes": "Needs help for spouse with mobility issues",
            "created": date.today(),
            "assigned_to": None,
            "status": "new",
            "progress": 0.35,
        },
        {
            "id": "LD-1002",
            "name": "Mary Smith",
            "origin": "phone",
            "city": "Seattle",
            "preference": "In-Home Care",
            "budget": 0,
            "timeline": "ASAP",
            "notes": "Daughter calling; fall risk",
            "created": date.today(),
            "assigned_to": "Advisor A",
            "status": "new",
            "progress": 0.70,
        },
        {
            "id": "LD-0999",
            "name": "Luis Alvarez",
            "origin": "app",
            "city": "Austin",
            "preference": "Memory Care",
            "budget": 5200,
            "timeline": "60 days",
            "notes": "Wandering behavior flagged in app",
            "created": date.today() - timedelta(days=1),
            "assigned_to": "Advisor B",
            "status": "in_progress",
            "progress": 0.15,
        },
    ]

def _seed_tasks():
    return [
        {"id": "T-1","title": "Call John Doe","lead_id": "LD-1001","priority": "High","due": date.today(),"origin": "app","done": False},
        {"id": "T-2","title": "Upload Disclosure for John Doe","lead_id": "LD-1001","priority": "Med","due": date.today(),"origin": "app","done": False},
        {"id": "T-3","title": "Call Mary Smith","lead_id": "LD-1002","priority": "High","due": date.today(),"origin": "phone","done": False},
        {"id": "T-4","title": "Complete intake for Luis Alvarez","lead_id": "LD-0999","priority": "Low","due": date.today() + timedelta(days=1),"origin": "app","done": False},
    ]
