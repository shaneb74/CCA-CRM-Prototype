
import streamlit as st
from data_loader import load_seed
from ui.widgets import section, table, pills

st.set_page_config(page_title="Client Record", page_icon="🗂️", layout="wide")
data = load_seed()
client = next(c for c in data["clients"] if c["name"]=="Margaret Holt")

st.header(f"{client['name']} — {client['city']}")
st.caption(f"Stage: {client['stage']}")

st.write("Flags: ", ", ".join(client["flags"]) or "None")

tabs = st.tabs(["Intake","Medical","Financial","Activities","Documents","Decision Support","Tours","Placement & Invoice"])

with tabs[0]:
    section("Intake")
    st.write({"Representative":"Linda Holt","Referral source":"Harborview DP","Preferred location":"Seattle Eastside"})
with tabs[1]:
    section("Medical profile")
    st.write({"Mobility":"Walker","Cognition":"Mild forgetfulness","Oxygen":"No","Diet":"Low sodium"})
with tabs[2]:
    section("Financial profile")
    st.write({"Monthly budget":"$4,500","Income":"$3,200","Assets":"$180,000"})
with tabs[3]:
    section("Activity log (mock)")
    st.write("- 2025-09-08 Called representative; left voicemail")
    st.write("- 2025-09-07 Received self-service intake")
with tabs[4]:
    section("Documents")
    docs = [d for d in data["documents"] if d["client_id"]==client["id"]]
    table(docs)
    st.button("New from template…", type="primary")
with tabs[5]:
    section("Decision Support — mock outputs")
    st.success("Recommendation: In-home care with support")
    st.write("Flags: fall risk")
    st.info("Monthly care cost: **$2,800** • Years funded: **9**")
    st.button("Run Guided Care Plan (mock)")
    st.button("Run Cost Planner (mock)")
with tabs[6]:
    section("Tours")
    st.warning("No tours scheduled yet.")
    st.button("Schedule tour…")
with tabs[7]:
    section("Placement & Invoice")
    st.write("No placement yet.")
    st.button("Create placement…")
