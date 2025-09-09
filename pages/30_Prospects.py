
import streamlit as st
from ui.widgets import inject_css, section
st.set_page_config(page_title="Prospects", page_icon="📇", layout="wide")
inject_css()
section("Prospect list")
st.dataframe([
 {"Category":"Discharge Planner","Name":"Jamie Ortega","Org":"Harborview MC","Last contact":"2025-09-05","MTD referrals":5},
 {"Category":"Clinic","Name":"Northlake Geriatrics","Org":"Northlake","Last contact":"2025-09-01","MTD referrals":2}], hide_index=True, use_container_width=True)
