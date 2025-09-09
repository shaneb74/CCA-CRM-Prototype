
import streamlit as st
from ui.widgets import inject_css, section
st.set_page_config(page_title="Communities", page_icon="🏠", layout="wide")
inject_css()
section("Directory")
items=[
 {"Name":"Cedar Grove Assisted Living","City":"Seattle, WA","Type":"AL","Capabilities":"dementia, hoyer, awake nights","Medicaid":"6 months"},
 {"Name":"Sunset Memory Care","City":"Bellevue, WA","Type":"MC","Capabilities":"dementia, secured, wander guard","Medicaid":"None"},
 {"Name":"Willow Adult Family Home","City":"Tacoma, WA","Type":"AFH","Capabilities":"wheelchair, 2-person transfer","Medicaid":"12 months"}]
q=st.text_input("Search by name, city, capability")
if q: items=[r for r in items if q.lower() in str(r).lower()]
st.dataframe(items, hide_index=True, use_container_width=True)
st.caption("Filters are display-only in this prototype.")
