
# 05_Supervisor_Workspace.py
import streamlit as st
st.set_page_config(page_title="Supervisor Workspace", page_icon="🧭", layout="wide")
from nav_bootstrap import boot; boot()

import store, random
store.init()

st.title("Supervisor Workspace")

advisors = sorted({l.get("assigned_to","Unassigned") or "Unassigned" for l in store.get_leads()} - {"Unassigned"})
if not advisors:
    advisors = ["Kelsey Jochum","Shane Bray","Alvarez White","R Patel","C Morgan","L Chen"]

tiles = st.columns(6)
for i,a in enumerate(advisors[:6]):
    with tiles[i]:
        a_leads = [l for l in store.get_leads() if (l.get("assigned_to") or "")==a]
        active = sum(1 for l in a_leads if l.get("stage") in ("Lead Received","Intake","Case Mgmt"))
        st.metric(a, active, "active cases")

st.subheader("Selected advisor")
pick = st.selectbox("Choose advisor", advisors, index=0, key="sup_pick")
focus = [l for l in store.get_leads() if (l.get("assigned_to") or "")==pick]
st.write(f"Open tasks for **{pick}**")
for l in focus[:5]:
    with st.container(border=True):
        st.write(f"**{l['name']}** — {l.get('stage','')} • {l.get('city','')}")
        st.caption(f"Intake progress")
        st.progress(float(l.get("intake_progress",0.0)))
