
# pages/20_Entity_Management.py
import streamlit as st
import communities_store as cstore
from ui_chrome import apply_chrome
apply_chrome()

st.set_page_config(page_title="Entity Management", page_icon="🗂️", layout="wide")
cstore.init()

st.title("Entity Management")
st.caption("Maintain communities for the prototype.")

q = st.text_input("Search communities", placeholder="Name/city/state")
results = cstore.search(q)

if results:
    import pandas as pd
    st.dataframe(pd.DataFrame([c.to_dict() for c in results]), use_container_width=True)
else:
    st.info("No results.")

# Export JSON of current communities
import json
if st.button("Export Communities (JSON)"):
    data = [c.to_dict() for c in cstore.all()]
    st.download_button("Download JSON", data=json.dumps(data, indent=2), file_name="communities_export.json")
