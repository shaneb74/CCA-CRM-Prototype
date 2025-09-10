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

# ---------------- Progress ----------------
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

# ---------------- Seeds ----------------
def _seed_leads():
    # 25 demo clients. Most are assigned to Advisors A-F; a couple are unassigned to demo "Assign to me".
    base = [
        {"id":"LD-1001","name":"John Doe","origin":"app","city":"Baton Rouge","preference":"Assisted Living","budget":4500,"timeline":"30 days","notes":"Needs help for spouse with mobility issues","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.35,"ds_recommendation":"Assisted Living","ds_est_cost":4500},
        {"id":"LD-1002","name":"Mary Smith","origin":"phone","city":"Seattle","preference":"In-Home Care","budget":0,"timeline":"ASAP","notes":"Daughter calling; fall risk","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.70,"ds_recommendation":"In-Home Care","ds_est_cost":8000},
        {"id":"LD-0999","name":"Luis Alvarez","origin":"app","city":"Austin","preference":"Memory Care","budget":5200,"timeline":"60 days","notes":"Wandering behavior flagged in app","created":date.today()-timedelta(days=1),"assigned_to":"Advisor B","status":"in_progress","progress":0.15,"ds_recommendation":"Memory Care","ds_est_cost":12500},
        {"id":"LD-1003","name":"Ava Johnson","origin":"hospital","city":"Chicago","preference":"Assisted Living","budget":6000,"timeline":"45 days","notes":"Recent discharge; PT scheduled","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.20,"ds_recommendation":"Assisted Living","ds_est_cost":6200},
        {"id":"LD-1004","name":"Noah Williams","origin":"app","city":"Denver","preference":"In-Home Care","budget":3000,"timeline":"90 days","notes":"Prefers evenings","created":date.today()-timedelta(days=2),"assigned_to":"Advisor C","status":"in_progress","progress":0.40,"ds_recommendation":"In-Home Care","ds_est_cost":5200},
        {"id":"LD-1005","name":"Emma Brown","origin":"phone","city":"Phoenix","preference":"Memory Care","budget":9000,"timeline":"ASAP","notes":"High wander risk","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.10,"ds_recommendation":"Memory Care","ds_est_cost":11000},
        {"id":"LD-1006","name":"Liam Davis","origin":"hospital","city":"Miami","preference":"Skilled Nursing","budget":13000,"timeline":"ASAP","notes":"Post-surgery rehab","created":date.today()-timedelta(days=3),"assigned_to":"Advisor D","status":"in_progress","progress":0.55,"ds_recommendation":"Assisted Living","ds_est_cost":7000},
        {"id":"LD-1007","name":"Olivia Martinez","origin":"app","city":"San Antonio","preference":"Assisted Living","budget":4800,"timeline":"30 days","notes":"Dietary restrictions","created":date.today(),"assigned_to":"Advisor B","status":"new","progress":0.25,"ds_recommendation":"Assisted Living","ds_est_cost":5100},
        {"id":"LD-1008","name":"Ethan Garcia","origin":"phone","city":"Dallas","preference":"In-Home Care","budget":4000,"timeline":"60 days","notes":"Prefers weekend calls","created":date.today()-timedelta(days=1),"assigned_to":"Advisor E","status":"in_progress","progress":0.33,"ds_recommendation":"In-Home Care","ds_est_cost":4600},
        {"id":"LD-1009","name":"Sophia Lee","origin":"app","city":"Portland","preference":"Memory Care","budget":10000,"timeline":"ASAP","notes":"Behavioral consult requested","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.05,"ds_recommendation":"Memory Care","ds_est_cost":13000},
        {"id":"LD-1010","name":"Mason Clark","origin":"app","city":"Nashville","preference":"Assisted Living","budget":5200,"timeline":"30 days","notes":"Hearing impaired","created":date.today(),"assigned_to":"Advisor C","status":"new","progress":0.12,"ds_recommendation":"Assisted Living","ds_est_cost":5400},
        {"id":"LD-1011","name":"Isabella Rodriguez","origin":"phone","city":"San Diego","preference":"In-Home Care","budget":3800,"timeline":"45 days","notes":"Spanish-speaking","created":date.today()-timedelta(days=1),"assigned_to":"Advisor D","status":"in_progress","progress":0.28,"ds_recommendation":"In-Home Care","ds_est_cost":4800},
        {"id":"LD-1012","name":"James Walker","origin":"hospital","city":"New York","preference":"Memory Care","budget":12000,"timeline":"ASAP","notes":"Neurologist referral","created":date.today(),"assigned_to":"Advisor F","status":"new","progress":0.18,"ds_recommendation":"Memory Care","ds_est_cost":12800},
        {"id":"LD-1013","name":"Mia Hall","origin":"app","city":"Atlanta","preference":"Assisted Living","budget":5000,"timeline":"60 days","notes":"Pet-friendly requirement","created":date.today()-timedelta(days=4),"assigned_to":"Advisor B","status":"in_progress","progress":0.45,"ds_recommendation":"Assisted Living","ds_est_cost":5300},
        {"id":"LD-1014","name":"Benjamin Allen","origin":"phone","city":"Charlotte","preference":"In-Home Care","budget":4200,"timeline":"30 days","notes":"Evening availability","created":date.today(),"assigned_to":"Advisor E","status":"new","progress":0.22,"ds_recommendation":"In-Home Care","ds_est_cost":4700},
        {"id":"LD-1015","name":"Charlotte Young","origin":"hospital","city":"Boston","preference":"Memory Care","budget":11500,"timeline":"ASAP","notes":"Worsening confusion","created":date.today()-timedelta(days=2),"assigned_to":"Advisor C","status":"in_progress","progress":0.36,"ds_recommendation":"Memory Care","ds_est_cost":11900},
        {"id":"LD-1016","name":"Henry King","origin":"app","city":"Cleveland","preference":"Assisted Living","budget":4800,"timeline":"90 days","notes":"Single-story preference","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.08,"ds_recommendation":"Assisted Living","ds_est_cost":5050},
        {"id":"LD-1017","name":"Amelia Wright","origin":"phone","city":"Tampa","preference":"In-Home Care","budget":5200,"timeline":"45 days","notes":"Needs PT coordination","created":date.today()-timedelta(days=1),"assigned_to":"Advisor D","status":"in_progress","progress":0.31,"ds_recommendation":"In-Home Care","ds_est_cost":5600},
        {"id":"LD-1018","name":"Alexander Scott","origin":"app","city":"Columbus","preference":"Assisted Living","budget":6200,"timeline":"30 days","notes":"Close to family","created":date.today(),"assigned_to":"Advisor F","status":"new","progress":0.14,"ds_recommendation":"Assisted Living","ds_est_cost":6400},
        {"id":"LD-1019","name":"Evelyn Green","origin":"phone","city":"Indianapolis","preference":"Memory Care","budget":9500,"timeline":"ASAP","notes":"Behavioral consult done","created":date.today()-timedelta(days=3),"assigned_to":"Advisor B","status":"in_progress","progress":0.52,"ds_recommendation":"Memory Care","ds_est_cost":10400},
        {"id":"LD-1020","name":"Daniel Baker","origin":"hospital","city":"Kansas City","preference":"Assisted Living","budget":5600,"timeline":"60 days","notes":"Discharge planner referral","created":date.today(),"assigned_to":"Advisor E","status":"new","progress":0.16,"ds_recommendation":"Assisted Living","ds_est_cost":5900},
        {"id":"LD-1021","name":"Harper Gonzalez","origin":"app","city":"Orlando","preference":"In-Home Care","budget":4400,"timeline":"30 days","notes":"Snowbird schedule","created":date.today()-timedelta(days=2),"assigned_to":"Advisor C","status":"in_progress","progress":0.42,"ds_recommendation":"In-Home Care","ds_est_cost":4800},
        {"id":"LD-1022","name":"Michael Perez","origin":"phone","city":"San Jose","preference":"Assisted Living","budget":7000,"timeline":"45 days","notes":"Prefers south side","created":date.today(),"assigned_to":"Advisor A","status":"new","progress":0.09,"ds_recommendation":"Assisted Living","ds_est_cost":7300},
        {"id":"LD-1023","name":"Abigail Rivera","origin":"hospital","city":"Philadelphia","preference":"Memory Care","budget":11800,"timeline":"ASAP","notes":"Geriatric psych consult","created":date.today()-timedelta(days=1),"assigned_to":"Advisor F","status":"in_progress","progress":0.48,"ds_recommendation":"Memory Care","ds_est_cost":12300},
        {"id":"LD-1024","name":"Sebastian Torres","origin":"app","city":"Las Vegas","preference":"In-Home Care","budget":5200,"timeline":"30 days","notes":"Night shift caregiver","created":date.today(),"assigned_to":"Advisor D","status":"new","progress":0.11,"ds_recommendation":"In-Home Care","ds_est_cost":5500},
        {"id":"LD-1025","name":"Luna Ramirez","origin":"phone","city":"Albuquerque","preference":"Assisted Living","budget":4800,"timeline":"60 days","notes":"Near daughter","created":date.today()-timedelta(days=2),"assigned_to":"Advisor E","status":"in_progress","progress":0.29,"ds_recommendation":"Assisted Living","ds_est_cost":5000},
    ]
    return base

def _seed_tasks():
    # Leave tasks reasonable; supervisor page uses live counts for Advisor A
    return [
        {"id": "T-1","title": "Call John Doe","lead_id": "LD-1001","priority": "High","due": date.today(),"origin": "app","done": False},
        {"id": "T-2","title": "Upload Disclosure for John Doe","lead_id": "LD-1001","priority": "Med","due": date.today(),"origin": "app","done": False},
        {"id": "T-3","title": "Call Mary Smith","lead_id": "LD-1002","priority": "High","due": date.today(),"origin": "phone","done": False},
        {"id": "T-4","title": "Complete intake for Luis Alvarez","lead_id": "LD-0999","priority": "Low","due": date.today() + timedelta(days=1),"origin": "app","done": False},
    ]
