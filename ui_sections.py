
# ui_sections.py — shared "data drawers" (compartments) used by workflows
import streamlit as st
import store

def _fmt_money(v):
    try:
        return f"${int(v):,}/month"
    except Exception:
        return v or "—"

def render_personal(lead):
    with st.container(border=True):
        st.subheader("Personal")
        c1, c2, c3 = st.columns([0.4,0.3,0.3])
        with c1:
            st.text_input("Name", value=lead.get("name",""), key=f"pers_name_{lead['id']}")
            st.text_input("City", value=lead.get("city",""), key=f"pers_city_{lead['id']}")
        with c2:
            st.selectbox("Status", ["new","in_progress","closed"], index=["new","in_progress","closed"].index(lead.get("status","new")), key=f"pers_status_{lead['id']}")
            st.text_input("Representative", value=lead.get("rep_name",""), key=f"pers_rep_{lead['id']}")
        with c3:
            st.text_input("Representative Phone", value=lead.get("rep_phone",""), key=f"pers_rphone_{lead['id']}")
            st.text_input("Representative Email", value=lead.get("rep_email",""), key=f"pers_remail_{lead['id']}")

def render_housing(lead):
    with st.container(border=True):
        st.subheader("Housing")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Current living arrangement", value=lead.get("housing_current",""), key=f"house_curr_{lead['id']}")
            st.text_input("Preferred geography", value=lead.get("preferred_geo",""), key=f"house_geo_{lead['id']}")
        with c2:
            st.text_input("Hospital/Discharge to", value=lead.get("discharge_to",""), key=f"house_discharge_{lead['id']}")
            st.text_area("Housing notes", value=lead.get("housing_notes",""), key=f"house_notes_{lead['id']}", height=80)

def render_medical(lead):
    with st.container(border=True):
        st.subheader("Medical")
        c1, c2, c3 = st.columns([0.4,0.3,0.3])
        with c1:
            st.text_input("Diagnosis", value=lead.get("diagnosis",""), key=f"med_dx_{lead['id']}")
            st.checkbox("Memory support needed", value=lead.get("care_needs",{}).get("memory", False), key=f"med_memory_{lead['id']}")
        with c2:
            st.text_input("Primary Doctor", value=lead.get("doctor",""), key=f"med_doc_{lead['id']}")
            st.text_input("Medications (comma sep)", value=lead.get("medications",""), key=f"med_meds_{lead['id']}")
        with c3:
            st.selectbox("Mobility", ["Independent","Needs assistance","Wheelchair"],
                         index=["Independent","Needs assistance","Wheelchair"].index(lead.get("mobility","Independent")),
                         key=f"med_mob_{lead['id']}")

def render_financial(lead):
    with st.container(border=True):
        st.subheader("Financial")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Budget (monthly)", value=str(lead.get("budget","")), key=f"fin_budget_{lead['id']}")
            st.text_input("Assets", value=lead.get("assets",""), key=f"fin_assets_{lead['id']}")
        with c2:
            st.text_input("Income sources", value=lead.get("income_sources",""), key=f"fin_income_{lead['id']}")
            st.text_input("Benefits", value=lead.get("benefits",""), key=f"fin_benefits_{lead['id']}")
        st.caption(f"Decision Support: {lead.get('ds_recommendation','—')} • Estimated cost: {_fmt_money(lead.get('ds_est_cost',''))}")

def render_lifestyle(lead):
    with st.container(border=True):
        st.subheader("Activities & Lifestyle")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Pets", value=lead.get("pets",""), key=f"life_pets_{lead['id']}")
            st.text_input("Dietary prefs", value=lead.get("diet",""), key=f"life_diet_{lead['id']}")
        with c2:
            st.text_input("Hobbies", value=lead.get("hobbies",""), key=f"life_hobbies_{lead['id']}")
            st.text_input("Notes", value=lead.get("lifestyle_notes",""), key=f"life_notes_{lead['id']}")

def render_notifications(lead):
    with st.container(border=True):
        st.subheader("Notifications & Notes")
        st.text_area("Advisor notes", value=lead.get("advisor_notes",""), key=f"note_adv_{lead['id']}", height=100)
        st.checkbox("RN assessor needed", value=lead.get("rn_needed", False), key=f"note_rn_{lead['id']}")

def render_placement(lead):
    with st.container(border=True):
        st.subheader("Placement / Communities")
        st.text_input("Shortlist communities (comma sep.)", value=lead.get("shortlist",""), key=f"place_shortlist_{lead['id']}")
        st.text_area("Tour outcomes", value=lead.get("tour_outcomes",""), key=f"place_outcomes_{lead['id']}", height=100)

def render_documents(lead):
    with st.container(border=True):
        st.subheader("Documents")
        st.caption("Use the real documents page for uploads in production. For now this is a placeholder.")
        st.text_area("Document notes", value=lead.get("doc_notes",""), key=f"docs_notes_{lead['id']}", height=80)

# Simple "save" that merges back to store; in real app you'd validate and persist
def save_from_session(lead_id):
    lead = store.get_lead(lead_id)
    # Pull a subset of edited fields back (keep this intentionally minimal)
    sess = st.session_state
    lead["rep_name"] = sess.get(f"pers_rep_{lead_id}", lead.get("rep_name"))
    lead["rep_phone"] = sess.get(f"pers_rphone_{lead_id}", lead.get("rep_phone"))
    lead["rep_email"] = sess.get(f"pers_remail_{lead_id}", lead.get("rep_email"))
    lead["housing_notes"] = sess.get(f"house_notes_{lead_id}", lead.get("housing_notes"))
    lead["diagnosis"] = sess.get(f"med_dx_{lead_id}", lead.get("diagnosis"))
    lead["mobility"] = sess.get(f"med_mob_{lead_id}", lead.get("mobility"))
    lead["advisor_notes"] = sess.get(f"note_adv_{lead_id}", lead.get("advisor_notes"))
    lead["shortlist"] = sess.get(f"place_shortlist_{lead_id}", lead.get("shortlist"))
    lead["tour_outcomes"] = sess.get(f"place_outcomes_{lead_id}", lead.get("tour_outcomes"))
    store.upsert_lead(lead)
    st.toast("Saved changes")
