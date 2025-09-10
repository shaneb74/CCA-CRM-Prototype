from ui_chrome import apply_chrome
apply_chrome()

import streamlit as st, store, random
store.init()

st.title("Supervisor Workspace")
advisors = sorted({l.get("assigned_to") or "Unassigned" for l in store.get_leads()})[:6]
cols = st.columns(3)
for i,name in enumerate(advisors):
    with cols[i%3]:
        with st.container(border=True):
            st.subheader(name)
            st.write(f"Open tasks: {random.randint(3,12)}")
            if st.button("View queue", key=f"q_{i}"):
                st.session_state["_goto_page"] = "pages/02_Advisor_Workspace.py"
                st.experimental_rerun()
