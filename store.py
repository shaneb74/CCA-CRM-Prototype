from datetime import date, timedelta
import streamlit as st

def init():
    if "leads" not in st.session_state:
        st.session_state.leads = _seed_leads()
    if "tasks" not in st.session_state:
        st.session_state.tasks = _seed_tasks()
    st.session_state.setdefault("selected_lead_id", None)
    st.session_state.setdefault("case_steps", {})

def get_leads():
    return st.session_state.leads

def get_lead(lead_id: str):
    return next((x for x in st.session_state.leads if x["id"] == lead_id), None)

def upsert_lead(updated: dict):
    leads = st.session_state.leads
    for i, l in enumerate(leads):
        if l["id"] == updated["id"]:
            leads[i] = updated
            return
    leads.append(updated)

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
        {"id": "LD-1001","name": "John Doe","origin": "app","city": "Baton Rouge","preference": "Assisted Living","budget": 4500,"timeline": "30 days","notes": "Needs help for spouse with mobility issues","created": date.today(),"assigned_to": None,"status": "new"},
        {"id": "LD-1002","name": "Mary Smith","origin": "phone","city": "Seattle","preference": "In-Home Care","budget": 0,"timeline": "ASAP","notes": "Daughter calling; fall risk","created": date.today(),"assigned_to": "Advisor A","status": "new"},
        {"id": "LD-0999","name": "Luis Alvarez","origin": "app","city": "Austin","preference": "Memory Care","budget": 5200,"timeline": "60 days","notes": "Wandering behavior flagged in app","created": date.today() - timedelta(days=1),"assigned_to": "Advisor B","status": "in_progress"},
    ]

def _seed_tasks():
    return [
        {"id": "T-1","title": "Call John Doe","lead_id": "LD-1001","priority": "High","due": date.today(),"origin": "app","done": False},
        {"id": "T-2","title": "Upload Disclosure for John Doe","lead_id": "LD-1001","priority": "Med","due": date.today(),"origin": "app","done": False},
        {"id": "T-3","title": "Call Mary Smith","lead_id": "LD-1002","priority": "High","due": date.today(),"origin": "phone","done": False},
        {"id": "T-4","title": "Complete intake for Luis Alvarez","lead_id": "LD-0999","priority": "Low","due": date.today() + timedelta(days=1),"origin": "app","done": False},
    ]
