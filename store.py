from datetime import date, timedelta
import streamlit as st

def init():
    if "leads" not in st.session_state:
        st.session_state.leads = _seed_leads()
    if "tasks" not in st.session_state:
        st.session_state.tasks = _seed_tasks()
    st.session_state.setdefault("selected_lead_id", None)
    st.session_state.setdefault("case_steps", {})

# ---------------- Leads ----------------
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

# Progress helpers (0..1)
def get_progress(lead_id: str) -> float:
    lead = get_lead(lead_id)
    return float(lead.get("progress", 0.0)) if lead else 0.0

def set_progress(lead_id: str, value: float):
    value = max(0.0, min(1.0, float(value)))
    lead = get_lead(lead_id)
    if lead:
        lead["progress"] = value
        upsert_lead(lead)

# ---------------- Tasks ----------------
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

# ---------------- Selection ----------------
def set_selected_lead(lead_id: str | None):
    st.session_state.selected_lead_id = lead_id

def get_selected_lead_id():
    return st.session_state.selected_lead_id

# ---------------- Seeds (10 leads) ----------------
def _seed_leads():
    # Deterministic demo dataset
    return [
        {"id":"LD-1001","name":"John Doe","origin":"app","city":"Baton Rouge","preference":"Assisted Living","budget":4500,"timeline":"30 days","notes":"Needs help for spouse with mobility issues","created":date.today(),"assigned_to":None,"status":"new","progress":0.35,"ds_recommendation":"Assisted Living","ds_est_cost":4500},
        {"id":"LD-1002","name":"Mary Smith","origin":"phone","city":"Seattle","preference":"In-Home Care","budget":0,"timeline":"ASAP","notes":"Daughter calling; fall risk","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.70,"ds_recommendation":"In-Home Care","ds_est_cost":8000},
        {"id":"LD-0999","name":"Luis Alvarez","origin":"app","city":"Austin","preference":"Memory Care","budget":5200,"timeline":"60 days","notes":"Wandering behavior flagged in app","created":date.today()-timedelta(days=1),"assigned_to":"Advisor B","status":"in_progress","progress":0.15,"ds_recommendation":"Memory Care","ds_est_cost":12500},
        {"id":"LD-1003","name":"Ava Johnson","origin":"hospital","city":"Chicago","preference":"Assisted Living","budget":6000,"timeline":"45 days","notes":"Recent discharge; PT scheduled","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.20,"ds_recommendation":"Assisted Living","ds_est_cost":6200},
        {"id":"LD-1004","name":"Noah Williams","origin":"app","city":"Denver","preference":"In-Home Care","budget":3000,"timeline":"90 days","notes":"Prefers evenings","created":date.today()-timedelta(days=2),"assigned_to":"Advisor C","status":"in_progress","progress":0.40,"ds_recommendation":"In-Home Care","ds_est_cost":5200},
        {"id":"LD-1005","name":"Emma Brown","origin":"phone","city":"Phoenix","preference":"Memory Care","budget":9000,"timeline":"ASAP","notes":"High wander risk","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.10,"ds_recommendation":"Memory Care","ds_est_cost":11000},
        {"id":"LD-1006","name":"Liam Davis","origin":"hospital","city":"Miami","preference":"Skilled Nursing","budget":13000,"timeline":"ASAP","notes":"Post-surgery rehab","created":date.today()-timedelta(days=3),"assigned_to":"Advisor D","status":"in_progress","progress":0.55,"ds_recommendation":"Assisted Living","ds_est_cost":7000},
        {"id":"LD-1007","name":"Olivia Martinez","origin":"app","city":"San Antonio","preference":"Assisted Living","budget":4800,"timeline":"30 days","notes":"Dietary restrictions","created":date.today(),"assigned_to":"Advisor B","status":"new","progress":0.25,"ds_recommendation":"Assisted Living","ds_est_cost":5100},
        {"id":"LD-1008","name":"Ethan Garcia","origin":"phone","city":"Dallas","preference":"In-Home Care","budget":4000,"timeline":"60 days","notes":"Prefers weekend calls","created":date.today()-timedelta(days=1),"assigned_to":"Advisor E","status":"in_progress","progress":0.33,"ds_recommendation":"In-Home Care","ds_est_cost":4600},
        {"id":"LD-1009","name":"Sophia Lee","origin":"app","city":"Portland","preference":"Memory Care","budget":10000,"timeline":"ASAP","notes":"Behavioral consult requested","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.05,"ds_recommendation":"Memory Care","ds_est_cost":13000},
    ]

def _seed_tasks():
    return [
        {"id": "T-1","title": "Call John Doe","lead_id": "LD-1001","priority": "High","due": date.today(),"origin": "app","done": False},
        {"id": "T-2","title": "Upload Disclosure for John Doe","lead_id": "LD-1001","priority": "Med","due": date.today(),"origin": "app","done": False},
        {"id": "T-3","title": "Call Mary Smith","lead_id": "LD-1002","priority": "High","due": date.today(),"origin": "phone","done": False},
        {"id": "T-4","title": "Complete intake for Luis Alvarez","lead_id": "LD-0999","priority": "Low","due": date.today() + timedelta(days=1),"origin": "app","done": False},
        {"id": "T-5","title": "Schedule tour for Ava Johnson","lead_id": "LD-1003","priority": "Med","due": date.today() + timedelta(days=2),"origin":"hospital","done": False},
        {"id": "T-6","title": "Send care plan to Emma Brown","lead_id": "LD-1005","priority": "High","due": date.today(),"origin":"phone","done": False},
        {"id": "T-7","title": "Follow up with Olivia Martinez","lead_id": "LD-1007","priority": "Med","due": date.today() + timedelta(days=1),"origin":"app","done": False},
        {"id": "T-8","title": "Confirm budget with Sophia Lee","lead_id": "LD-1009","priority": "High","due": date.today(),"origin":"app","done": False},
    ]
