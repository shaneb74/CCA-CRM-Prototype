# ui_sections.py — reusable, namespaced "data drawers" to avoid DuplicateWidgetID
import streamlit as st, store
def _k(base, lead_id, ns): return f"{base}_{lead_id}_{ns}"
def personal(lead, ns="main"):
    with st.container(border=True):
        st.subheader("Personal"); c1,c2,c3=st.columns([0.45,0.3,0.25])
        with c1: st.text_input("Full name", value=lead.get("name",""), key=_k("name",lead["id"],ns)); st.text_input("City", value=lead.get("city",""), key=_k("city",lead["id"],ns))
        with c2: st.selectbox("Status", ["new","in_progress","closed"], index=["new","in_progress","closed"].index(lead.get("status","new")), key=_k("status",lead["id"],ns)); st.text_input("Assigned to", value=lead.get("assigned_to",""), key=_k("assignee",lead["id"],ns))
        with c3: st.text_input("Budget / mo", value=str(lead.get("budget","")), key=_k("budget",lead["id"],ns)); st.text_input("Priority", value=str(lead.get("priority","")), key=_k("prio",lead["id"],ns))
def medical(lead, ns="main"):
    with st.container(border=True):
        st.subheader("Care needs"); st.checkbox("Memory support needed", value=lead.get("care_needs",{}).get("memory",False), key=_k("mem",lead["id"],ns)); st.text_area("Notes", value=lead.get("care_notes",""), key=_k("care_notes",lead["id"],ns), height=100)
def financial(lead, ns="main"):
    with st.container(border=True):
        st.subheader("Financial"); st.text_input("Monthly budget", value=str(lead.get("budget","")), key=_k("fin_budget",lead["id"],ns)); st.text_input("Assets", value=lead.get("assets",""), key=_k("assets",lead["id"],ns))
def lifestyle(lead, ns="main"):
    with st.container(border=True):
        st.subheader("Lifestyle"); st.text_input("Hobbies", value=lead.get("hobbies",""), key=_k("hobby",lead["id"],ns)); st.text_input("Pets", value=lead.get("pets",""), key=_k("pets",lead["id"],ns))
def notes(lead, ns="main"):
    with st.container(border=True):
        st.subheader("Advisor notes"); st.text_area("Notes", value=lead.get("advisor_notes",""), key=_k("adv_notes",lead["id"],ns), height=120)
def save_some(lead_id):
    lead = store.get_lead(lead_id); ss = st.session_state
    lead["advisor_notes"] = ss.get(f"adv_notes_{lead_id}_main", ss.get(f"adv_notes_{lead_id}_drawer", lead.get("advisor_notes")))
    lead["budget"]        = ss.get(f"fin_budget_{lead_id}_main", ss.get(f"fin_budget_{lead_id}_drawer", lead.get("budget")))
    store.upsert_lead(lead); st.toast("Saved")