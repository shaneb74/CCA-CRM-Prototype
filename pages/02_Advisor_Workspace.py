from ui_chrome import apply_chrome
apply_chrome()

import streamlit as st
import store

store.init()
st.title("Advisor Workspace")

leads = store.get_leads()
left, right = st.columns([1,2])

with left:
    st.subheader("Work Queue")
    for l in leads[:10]:
        with st.container(border=True):
            st.caption(f"{l.get('city','')} • Next: start intake")
            cols = st.columns([1,1])
            if cols[0].button("Open", key=f"open_{l['id']}"):
                store.set_selected_lead(l["id"])
                st.session_state["_goto_page"] = "pages/89_Workflows.py"
                st.experimental_rerun()
            if cols[1].button("Client Record", key=f"rec_{l['id']}"):
                store.set_selected_lead(l["id"])
                st.session_state["_goto_page"] = "pages/04_Client_Record.py"
                st.experimental_rerun()

with right:
    st.subheader("Case Overview")
    sid = store.get_selected_lead_id()
    lead = store.get_lead(sid) if sid else (leads[0] if leads else None)
    if not lead:
        st.info("Select a lead on the left.")
    else:
        st.write(f"**{lead['name']} • {lead.get('city','')}**")
        st.progress(lead.get("progress",0.0))
        st.write("Decision support (last results):")
        st.info(f"Recommended: {lead.get('ds_recommendation', '—')}  •  Estimated cost: ${int(lead.get('ds_est_cost',0)):,}/month")
        if st.button("Open full client record"):
            st.session_state["_goto_page"] = "pages/04_Client_Record.py"
            st.experimental_rerun()
