
# pages/91_Placement_Workflow.py
import streamlit as st
import communities_store as cstore
import store

st.set_page_config(page_title="Placement Workflow", page_icon="🏙️", layout="wide")
store.init(); cstore.init()

lead_id = store.get_selected_lead_id()
if not lead_id:
    st.info("Select a client first in Client Record.")
    st.stop()

lead = store.get_lead(lead_id)
st.title("Placement Workflow")
st.caption(f"{lead.get('name','')} — {lead.get('city','')}")

shortlist = st.session_state.get("community_shortlist", [])

left, mid, right = st.columns([3,6,3], gap="large")

with left:
    st.subheader("Filters")
    q = st.text_input("Search", key="pl_q")
    results = cstore.search(q)

with mid:
    st.subheader("Matches")
    for c in results:
        with st.container(border=True):
            st.write(f"**{c.name}** • {c.type} — {c.city}, {c.state}")
            if st.button("Add to shortlist", key=f"add_{c.id}"):
                if c.id not in shortlist:
                    st.session_state.community_shortlist.append(c.id)

with right:
    st.subheader("Shortlist")
    for cid in shortlist:
        c = cstore.get(cid)
        if c:
            st.write(f"{c.name} • {c.city}")
            if st.button("Remove", key=f"rm_{cid}"):
                st.session_state.community_shortlist = [x for x in shortlist if x!=cid]
