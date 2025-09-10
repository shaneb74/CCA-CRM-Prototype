# store.py — now backed by models.py for safer extensibility
from datetime import date, timedelta
import streamlit as st
from models import Lead, Task, Advisor, Origin, Status, Priority


# NEW: central chrome injection for all pages
try:
    from ui_chrome import apply_chrome
    apply_chrome()
except Exception:
    pass

# --- App-wide "current user" (mock) ---
CURRENT_USER = "Kelsey Jochum"

# --- Real advisor names (from internal focus docs) ---
ADVISORS = [
    "Kelsey Jochum",
    "Jennifer James",
    "Jenny Krzemien",
    "Chanda Hickman",
    "Stephanie Holm",
    "Jesiah Irish",
    "Marta Street",
    "Jennifer White",
]

def _assign(i: int) -> str:
    # Deterministic round-robin for demo stability
    return ADVISORS[i % len(ADVISORS)]

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

# ---------------- Seeds (25 leads; assigned across named advisors) ----------------
def _seed_leads():
    base = [
        Lead(id="LD-1001", name="John Doe", origin=Origin.APP, city="Baton Rouge",
             preference="Assisted Living", budget=4500, timeline="30 days",
             notes="Needs help for spouse with mobility issues",
             assigned_to=_assign(0), status=Status.NEW, progress=0.35,
             ds_recommendation="Assisted Living", ds_est_cost=4500,
             attrs={"insurance":"Medicare Advantage","language":"English"}).to_dict(),

        Lead(id="LD-1002", name="Mary Smith", origin=Origin.PHONE, city="Seattle",
             preference="In-Home Care", budget=0, timeline="ASAP",
             notes="Daughter calling; fall risk",
             assigned_to=_assign(1), status=Status.NEW, progress=0.70,
             ds_recommendation="In-Home Care", ds_est_cost=8000,
             attrs={"preferred_contact_time":"Mornings"}).to_dict(),

        Lead(id="LD-0999", name="Luis Alvarez", origin=Origin.APP, city="Austin",
             preference="Memory Care", budget=5200, timeline="60 days",
             notes="Wandering behavior flagged in app",
             assigned_to=_assign(2), status=Status.IN_PROGRESS, progress=0.15,
             ds_recommendation="Memory Care", ds_est_cost=12500).to_dict(),

        Lead(id="LD-1003", name="Ava Johnson", origin=Origin.HOSPITAL, city="Chicago",
             preference="Assisted Living", budget=6000, timeline="45 days",
             notes="Recent discharge; PT scheduled",
             assigned_to=_assign(3), status=Status.NEW, progress=0.20,
             ds_recommendation="Assisted Living", ds_est_cost=6200).to_dict(),

        Lead(id="LD-1004", name="Noah Williams", origin=Origin.APP, city="Denver",
             preference="In-Home Care", budget=3000, timeline="90 days",
             notes="Prefers evenings",
             assigned_to=_assign(4), status=Status.IN_PROGRESS, progress=0.40,
             ds_recommendation="In-Home Care", ds_est_cost=5200).to_dict(),

        Lead(id="LD-1005", name="Emma Brown", origin=Origin.PHONE, city="Phoenix",
             preference="Memory Care", budget=9000, timeline="ASAP",
             notes="High wander risk",
             assigned_to=_assign(5), status=Status.NEW, progress=0.10,
             ds_recommendation="Memory Care", ds_est_cost=11000).to_dict(),

        Lead(id="LD-1006", name="Liam Davis", origin=Origin.HOSPITAL, city="Miami",
             preference="Skilled Nursing", budget=13000, timeline="ASAP",
             notes="Post-surgery rehab",
             assigned_to=_assign(6), status=Status.IN_PROGRESS, progress=0.55,
             ds_recommendation="Assisted Living", ds_est_cost=7000).to_dict(),

        Lead(id="LD-1007", name="Olivia Martinez", origin=Origin.APP, city="San Antonio",
             preference="Assisted Living", budget=4800, timeline="30 days",
             notes="Dietary restrictions",
             assigned_to=_assign(7), status=Status.NEW, progress=0.25,
             ds_recommendation="Assisted Living", ds_est_cost=5100).to_dict(),

        Lead(id="LD-1008", name="Ethan Garcia", origin=Origin.PHONE, city="Dallas",
             preference="In-Home Care", budget=4000, timeline="60 days",
             notes="Prefers weekend calls",
             assigned_to=_assign(8), status=Status.IN_PROGRESS, progress=0.33,
             ds_recommendation="In-Home Care", ds_est_cost=4600).to_dict(),

        Lead(id="LD-1009", name="Sophia Lee", origin=Origin.APP, city="Portland",
             preference="Memory Care", budget=10000, timeline="ASAP",
             notes="Behavioral consult requested",
             assigned_to=_assign(9), status=Status.NEW, progress=0.05,
             ds_recommendation="Memory Care", ds_est_cost=13000).to_dict(),
        # ... continue same pattern up to 25 as previously seeded ...
    ]

    # pad out to 25 by cloning patterns deterministically to keep length short here
    ids = [("LD-1010","Mason Clark","Nashville","Assisted Living",5200, "30 days", "Hearing impaired", 0.12, "Assisted Living", 5400, Origin.APP),
           ("LD-1011","Isabella Rodriguez","San Diego","In-Home Care",3800, "45 days", "Spanish-speaking", 0.28, "In-Home Care", 4800, Origin.PHONE),
           ("LD-1012","James Walker","New York","Memory Care",12000, "ASAP", "Neurologist referral", 0.18, "Memory Care", 12800, Origin.HOSPITAL),
           ("LD-1013","Mia Hall","Atlanta","Assisted Living",5000, "60 days", "Pet-friendly requirement", 0.45, "Assisted Living", 5300, Origin.APP),
           ("LD-1014","Benjamin Allen","Charlotte","In-Home Care",4200, "30 days", "Evening availability", 0.22, "In-Home Care", 4700, Origin.PHONE),
           ("LD-1015","Charlotte Young","Boston","Memory Care",11500, "ASAP", "Worsening confusion", 0.36, "Memory Care", 11900, Origin.HOSPITAL),
           ("LD-1016","Henry King","Cleveland","Assisted Living",4800, "90 days", "Single-story preference", 0.08, "Assisted Living", 5050, Origin.APP),
           ("LD-1017","Amelia Wright","Tampa","In-Home Care",5200, "45 days", "Needs PT coordination", 0.31, "In-Home Care", 5600, Origin.PHONE),
           ("LD-1018","Alexander Scott","Columbus","Assisted Living",6200, "30 days", "Close to family", 0.14, "Assisted Living", 6400, Origin.APP),
           ("LD-1019","Evelyn Green","Indianapolis","Memory Care",9500, "ASAP", "Behavioral consult done", 0.52, "Memory Care", 10400, Origin.PHONE),
           ("LD-1020","Daniel Baker","Kansas City","Assisted Living",5600, "60 days", "Discharge planner referral", 0.16, "Assisted Living", 5900, Origin.HOSPITAL),
           ("LD-1021","Harper Gonzalez","Orlando","In-Home Care",4400, "30 days", "Snowbird schedule", 0.42, "In-Home Care", 4800, Origin.APP),
           ("LD-1022","Michael Perez","San Jose","Assisted Living",7000, "45 days", "Prefers south side", 0.09, "Assisted Living", 7300, Origin.PHONE),
           ("LD-1023","Abigail Rivera","Philadelphia","Memory Care",11800, "ASAP", "Geriatric psych consult", 0.48, "Memory Care", 12300, Origin.HOSPITAL),
           ("LD-1024","Sebastian Torres","Las Vegas","In-Home Care",5200, "30 days", "Night shift caregiver", 0.11, "In-Home Care", 5500, Origin.APP),
           ("LD-1025","Luna Ramirez","Albuquerque","Assisted Living",4800, "60 days", "Near daughter", 0.29, "Assisted Living", 5000, Origin.PHONE)]
    for i, tup in enumerate(ids, start=10):
        lid, name, city, pref, budget, timeline, notes, prog, dsr, dsc, orig = tup
        base.append(
            Lead(id=lid, name=name, origin=orig, city=city,
                 preference=pref, budget=budget, timeline=timeline, notes=notes,
                 assigned_to=_assign(i), status=Status.IN_PROGRESS if prog>0.2 else Status.NEW,
                 progress=prog, ds_recommendation=dsr, ds_est_cost=dsc).to_dict()
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
             due=date.today() + timedelta(days=1), origin=Origin.APP).to_dict(),
    ]
