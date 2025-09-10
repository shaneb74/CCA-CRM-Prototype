
# ui_sections.py — reusable "data drawers" used by workflows
import streamlit as st
import store

def _ns(key: str, lead_id: str, ns: str|None=None):
    suffix = f"_{ns}" if ns else ""
    return f"{key}_{lead_id}{suffix}"

def render_personal(lead, ns=None):
    with st.container(border=True):
        st.subheader("Personal")
        c1, c2, c3 = st.columns([0.5,0.25,0.25])
        with c1:
            st.text_input("Name", value=lead.get("name",""), key=_ns("pers_name",lead['id'],ns))
            st.text_input("City", value=lead.get("city",""), key=_ns("pers_city",lead['id'],ns))
        with c2:
            st.selectbox("Stage", ["Lead Received","Intake","Case Mgmt","Closed"],
                         index=["Lead Received","Intake","Case Mgmt","Closed"].index(lead.get("stage","Lead Received")),
                         key=_ns("pers_stage",lead['id'],ns))
            st.text_input("Assigned to", value=lead.get("assigned_to",""), key=_ns("pers_assigned",lead['id'],ns))
        with c3:
            st.text_input("Priority", value=str(lead.get("priority","")), key=_ns("pers_prio",lead['id'],ns))
            st.text_input("Budget", value=str(lead.get("budget","")), key=_ns("pers_budget",lead['id'],ns))

def render_medical(lead, ns=None):
    with st.container(border=True):
        st.subheader("Care needs")
        st.checkbox("Memory support needed", value=lead.get("care_needs",{}).get("memory",False), key=_ns("med_memory",lead['id'],ns))
        st.text_area("Notes", value=lead.get("care_notes",""), key=_ns("med_notes",lead['id'],ns), height=100)

def render_financial(lead, ns=None):
    with st.container(border=True):
        st.subheader("Financial")
        st.text_input("Monthly budget", value=str(lead.get("budget","")), key=_ns("fin_budget",lead['id'],ns))
        st.text_input("Assets", value=lead.get("assets",""), key=_ns("fin_assets",lead['id'],ns))

def render_lifestyle(lead, ns=None):
    with st.container(border=True):
        st.subheader("Lifestyle")
        st.text_input("Hobbies", value=lead.get("hobbies",""), key=_ns("life_hobby",lead['id'],ns))
        st.text_input("Pets", value=lead.get("pets",""), key=_ns("life_pets",lead['id'],ns))

def render_notifications(lead, ns=None):
    with st.container(border=True):
        st.subheader("Communications / Notes")
        st.text_area("Advisor notes", value=lead.get("advisor_notes",""), key=_ns("note_adv",lead['id'],ns), height=120)

def save_from_session(lead_id):
    # This demo saver copies a few edited fields back into the store
    lead = store.get_lead(lead_id)
    ss = st.session_state
    def pick(base):
        return ss.get(f"{base}_{lead_id}_main", ss.get(f"{base}_{lead_id}_drawer", None))
    lead["advisor_notes"] = pick("note_adv") or lead.get("advisor_notes")
    lead["budget"] = pick("fin_budget") or lead.get("budget")
    store.upsert_lead(lead)
    st.toast("Saved changes")
