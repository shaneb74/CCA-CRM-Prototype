
# ui_sections.py — shared "data drawers" (compartments) with key namespaces
import streamlit as st
import store

def _ns(key: str, lead_id: str, ns: str|None=None):
    """Build a unique session-state key with optional namespace to avoid duplicates
    when the same component is rendered in two places on the same page."""
    suffix = f"_{ns}" if ns else ""
    return f"{key}_{lead_id}{suffix}"

def _fmt_money(v):
    try:
        return f"${int(v):,}/month"
    except Exception:
        return v or "—"

def render_personal(lead, ns: str|None=None):
    with st.container(border=True):
        st.subheader("Personal")
        c1, c2, c3 = st.columns([0.4,0.3,0.3])
        with c1:
            st.text_input("Name", value=lead.get("name",""), key=_ns("pers_name", lead['id'], ns))
            st.text_input("City", value=lead.get("city",""), key=_ns("pers_city", lead['id'], ns))
        with c2:
            st.selectbox("Status", ["new","in_progress","closed"],
                         index=["new","in_progress","closed"].index(lead.get("status","new")),
                         key=_ns("pers_status", lead['id'], ns))
            st.text_input("Representative", value=lead.get("rep_name",""), key=_ns("pers_rep", lead['id'], ns))
        with c3:
            st.text_input("Representative Phone", value=lead.get("rep_phone",""), key=_ns("pers_rphone", lead['id'], ns))
            st.text_input("Representative Email", value=lead.get("rep_email",""), key=_ns("pers_remail", lead['id'], ns))

def render_housing(lead, ns: str|None=None):
    with st.container(border=True):
        st.subheader("Housing")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Current living arrangement", value=lead.get("housing_current",""), key=_ns("house_curr", lead['id'], ns))
            st.text_input("Preferred geography", value=lead.get("preferred_geo",""), key=_ns("house_geo", lead['id'], ns))
        with c2:
            st.text_input("Hospital/Discharge to", value=lead.get("discharge_to",""), key=_ns("house_discharge", lead['id'], ns))
            st.text_area("Housing notes", value=lead.get("housing_notes",""), key=_ns("house_notes", lead['id'], ns), height=80)

def render_medical(lead, ns: str|None=None):
    with st.container(border=True):
        st.subheader("Medical")
        c1, c2, c3 = st.columns([0.4,0.3,0.3])
        with c1:
            st.text_input("Diagnosis", value=lead.get("diagnosis",""), key=_ns("med_dx", lead['id'], ns))
            st.checkbox("Memory support needed", value=lead.get("care_needs",{}).get("memory", False), key=_ns("med_memory", lead['id'], ns))
        with c2:
            st.text_input("Primary Doctor", value=lead.get("doctor",""), key=_ns("med_doc", lead['id'], ns))
            st.text_input("Medications (comma sep)", value=lead.get("medications",""), key=_ns("med_meds", lead['id'], ns))
        with c3:
            st.selectbox("Mobility", ["Independent","Needs assistance","Wheelchair"],
                         index=["Independent","Needs assistance","Wheelchair"].index(lead.get("mobility","Independent")),
                         key=_ns("med_mob", lead['id'], ns))

def render_financial(lead, ns: str|None=None):
    with st.container(border=True):
        st.subheader("Financial")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Budget (monthly)", value=str(lead.get("budget","")), key=_ns("fin_budget", lead['id'], ns))
            st.text_input("Assets", value=lead.get("assets",""), key=_ns("fin_assets", lead['id'], ns))
        with c2:
            st.text_input("Income sources", value=lead.get("income_sources",""), key=_ns("fin_income", lead['id'], ns))
            st.text_input("Benefits", value=lead.get("benefits",""), key=_ns("fin_benefits", lead['id'], ns))
        st.caption(f"Decision Support: {lead.get('ds_recommendation','—')} • Estimated cost: {_fmt_money(lead.get('ds_est_cost',''))}")

def render_lifestyle(lead, ns: str|None=None):
    with st.container(border=True):
        st.subheader("Activities & Lifestyle")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Pets", value=lead.get("pets",""), key=_ns("life_pets", lead['id'], ns))
            st.text_input("Dietary prefs", value=lead.get("diet",""), key=_ns("life_diet", lead['id'], ns))
        with c2:
            st.text_input("Hobbies", value=lead.get("hobbies",""), key=_ns("life_hobbies", lead['id'], ns))
            st.text_input("Notes", value=lead.get("lifestyle_notes",""), key=_ns("life_notes", lead['id'], ns))

def render_notifications(lead, ns: str|None=None):
    with st.container(border=True):
        st.subheader("Notifications & Notes")
        st.text_area("Advisor notes", value=lead.get("advisor_notes",""), key=_ns("note_adv", lead['id'], ns), height=100)
        st.checkbox("RN assessor needed", value=lead.get("rn_needed", False), key=_ns("note_rn", lead['id'], ns))

def render_placement(lead, ns: str|None=None):
    with st.container(border=True):
        st.subheader("Placement / Communities")
        st.text_input("Shortlist communities (comma sep.)", value=lead.get("shortlist",""), key=_ns("place_shortlist", lead['id'], ns))
        st.text_area("Tour outcomes", value=lead.get("tour_outcomes",""), key=_ns("place_outcomes", lead['id'], ns), height=100)

def render_documents(lead, ns: str|None=None):
    with st.container(border=True):
        st.subheader("Documents")
        st.caption("Use the real documents page for uploads in production. For now this is a placeholder.")
        st.text_area("Document notes", value=lead.get("doc_notes",""), key=_ns("docs_notes", lead['id'], ns), height=80)

def save_from_session(lead_id):
    lead = store.get_lead(lead_id)
    sess = st.session_state
    # Try both main and drawer keys (we only copy if present)
    def pick(base):
        return sess.get(f"{base}_{lead_id}_main", sess.get(f"{base}_{lead_id}_drawer", None))
    lead["rep_name"] = pick("pers_rep") or lead.get("rep_name")
    lead["rep_phone"] = pick("pers_rphone") or lead.get("rep_phone")
    lead["rep_email"] = pick("pers_remail") or lead.get("rep_email")
    lead["housing_notes"] = pick("house_notes") or lead.get("housing_notes")
    lead["diagnosis"] = pick("med_dx") or lead.get("diagnosis")
    lead["mobility"] = pick("med_mob") or lead.get("mobility")
    lead["advisor_notes"] = pick("note_adv") or lead.get("advisor_notes")
    lead["shortlist"] = pick("place_shortlist") or lead.get("shortlist")
    lead["tour_outcomes"] = pick("place_outcomes") or lead.get("tour_outcomes")
    store.upsert_lead(lead)
    st.toast("Saved changes")
