
from datetime import date, timedelta
import streamlit as st
from models import Lead, Task, Origin, Status, Priority

CURRENT_USER = "Kelsey Jochum"

ADVISORS = [
    "Kelsey Jochum","Jennifer James","Jenny Krzemien","Chanda Hickman",
    "Stephanie Holm","Jesiah Irish","Marta Street","Jennifer White"
]

def _assign(i:int)->str: return ADVISORS[i % len(ADVISORS)]

def init():
    if "leads" not in st.session_state: st.session_state.leads = _seed_leads()
    if "tasks" not in st.session_state: st.session_state.tasks = _seed_tasks()
    if "notifications" not in st.session_state: st.session_state.notifications = _seed_notifications()
    st.session_state.setdefault("selected_lead_id", None)
    st.session_state.setdefault("case_steps", {})

# ---- Lead access ----
def get_leads(): return st.session_state.leads
def get_lead(lead_id:str):
    return next((x for x in st.session_state.leads if x["id"]==lead_id), None)
def upsert_lead(updated:dict):
    for i,l in enumerate(st.session_state.leads):
        if l["id"]==updated["id"]:
            st.session_state.leads[i]=updated; return
    st.session_state.leads.append(updated)
def set_selected_lead(lead_id:str|None): st.session_state.selected_lead_id = lead_id
def get_selected_lead_id(): return st.session_state.selected_lead_id

# ---- Tasks ----
def get_tasks(active_only=True):
    t=st.session_state.tasks
    return [x for x in t if not x.get("done")] if active_only else t

# ---- Notifications ----
def get_notifications(): return st.session_state.get("notifications", [])

# ---- Seeds ----
def _seed_leads():
    base=[
        Lead(id="LD-1001", name="John Doe", origin=Origin.APP, city="Baton Rouge",
             preference="Assisted Living", budget=4500, timeline="30 days",
             notes="Needs help for spouse with mobility issues",
             assigned_to=_assign(0), status=Status.NEW, progress=0.35,
             ds_recommendation="Assisted Living", ds_est_cost=4500).to_dict(),
        Lead(id="LD-1002", name="Mary Smith", origin=Origin.PHONE, city="Seattle",
             preference="In-Home Care", budget=0, timeline="ASAP",
             notes="Daughter calling; fall risk", assigned_to=_assign(1),
             status=Status.NEW, progress=0.70, ds_recommendation="In-Home Care",
             ds_est_cost=8000).to_dict(),
        Lead(id="LD-0999", name="Luis Alvarez", origin=Origin.APP, city="Austin",
             preference="Memory Care", budget=5200, timeline="60 days",
             notes="Wandering behavior flagged in app", assigned_to=_assign(2),
             status=Status.IN_PROGRESS, progress=0.15, ds_recommendation="Memory Care",
             ds_est_cost=12500).to_dict(),
    ]
    # Pad to a friendly list
    cities=["Chicago","Denver","Phoenix","Miami","San Antonio","Dallas","Portland"]
    prefs=["Assisted Living","Memory Care","In-Home Care"]
    costs=[5200,11000,7000,5100,4600,13000]
    for i in range(3,16):
        base.append(
            Lead(id=f"LD-10{i:02d}", name=f"Client {i}", origin=Origin.APP, city=cities[i%len(cities)],
                 preference=prefs[i%len(prefs)], budget=costs[i%len(costs)],
                 timeline="45 days", notes="—", assigned_to=_assign(i),
                 status=Status.IN_PROGRESS if i%2 else Status.NEW, progress=0.2+(i%5)*0.12,
                 ds_recommendation=prefs[(i+1)%len(prefs)], ds_est_cost=costs[(i+2)%len(costs)]).to_dict()
        )
    return base

def _seed_tasks():
    return [
        Task(id="T-1", title="Call John Doe", lead_id="LD-1001", priority=Priority.HIGH,
             due=date.today(), origin=Origin.APP).to_dict(),
        Task(id="T-2", title="Upload Disclosure for John Doe", lead_id="LD-1001", priority=Priority.MED,
             due=date.today(), origin=Origin.APP).to_dict(),
        Task(id="T-3", title="Call Mary Smith", lead_id="LD-1002", priority=Priority.HIGH,
             due=date.today(), origin=Origin.PHONE).to_dict(),
        Task(id="T-4", title="Complete intake for Luis Alvarez", lead_id="LD-0999", priority=Priority.LOW,
             due=date.today()+timedelta(days=1), origin=Origin.APP).to_dict(),
    ]

def _seed_notifications():
    return [
        {"id":"N-1","text":"Upload signed Disclosure before scheduling tours.","kind":"compliance"},
        {"id":"N-2","text":"Confirm Medicaid rollover during financial review.","kind":"financial"},
        {"id":"N-3","text":"Keep intake notes date-stamped with initials.","kind":"general"},
    ]
