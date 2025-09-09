
import streamlit as st
from ui.widgets import inject_css, section
from data_loader import load_seed
st.set_page_config(page_title="Client Record", page_icon="🗂️", layout="wide")
inject_css()
data = load_seed()
client = next(c for c in data["clients"] if c["name"]=="Margaret Holt")
st.header(f"{client['name']} — {client['city']}")
st.caption(f"Stage: {client['stage']} | Flags: {', '.join(client['flags']) or 'None'}")
tabs = st.tabs(["Intake","Medical","Financial","Activities","Documents","Decision Support","Tours","Placement & Invoice"])
with tabs[0]: section("Intake"); st.write({"Representative":"Linda Holt","Referral source":"Harborview DP","Preferred location":"Seattle Eastside"})
with tabs[1]: section("Medical profile"); st.write({"Mobility":"Walker","Cognition":"Mild forgetfulness","Oxygen":"No","Diet":"Low sodium"})
with tabs[2]: section("Financial profile"); st.write({"Monthly budget":"$4,500","Income":"$3,200","Assets":"$180,000"})
with tabs[3]: section("Activity log (mock)"); st.write("- 2025-09-08 Called representative; left voicemail"); st.write("- 2025-09-07 Received self-service intake")
with tabs[4]: section("Documents"); docs=[d for d in data["documents"] if d["client_id"]==client["id"]]; st.dataframe(docs, hide_index=True, use_container_width=True)
with tabs[5]: section("Decision Support — mock outputs"); st.success("Recommendation: In-home care with support"); st.info("Monthly care cost: **$2,800** • Years funded: **9**")
with tabs[6]: section("Tours"); st.warning("No tours scheduled yet.")
with tabs[7]: section("Placement & Invoice"); st.write("No placement yet.")
