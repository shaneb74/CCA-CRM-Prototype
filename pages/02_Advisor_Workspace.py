# 02_Advisor_Workspace.py — button label updated
import streamlit as st
import store
from ui_chrome import apply_chrome
apply_chrome()  # idempotent

store.init()

st.title("Advisor Workspace")
st.markdown(
    '<style>.page {max-width:1200px;margin:0 auto}.summary-card{border:1px solid #e5e7eb;border-radius:14px;padding:16px;background:#fff}</style>',
    unsafe_allow_html=True,
)
st.markdown('<div class="page">', unsafe_allow_html=True)

def segmented(label, options, default):
    if hasattr(st, "segmented_control"):
        return st.segmented_control(label, options=options, default=default)
    return st.radio(label, options, index=options.index(default), horizontal=True)

f1, f2 = st.columns([0.6, 0.4])
with f1:
    origin = segmented("Filter", ["All leads","App","Phone","Hospital"], "All leads")
with f2:
    stage = segmented("Stage", ["All","Lead Received","Intake","Case Mgmt"], "All")

def origin_ok(o):
    if origin == "All leads": return True
    return o == {"App":"app","Phone":"phone","Hospital":"hospital"}[origin]

leads = [l for l in store.get_leads() if origin_ok(l["origin"])]

sel_id = st.session_state.get("ws_selected_lead") or (leads[0]["id"] if leads else None)
if sel_id and not any(l["id"] == sel_id for l in leads):
    sel_id = leads[0]["id"] if leads else None
st.session_state["ws_selected_lead"] = sel_id

left, right = st.columns([0.44, 0.56])

with left:
    st.subheader("Work Queue")
    for l in leads:
        with st.container(border=True):
            st.markdown(f"**{l['name']} — {('Intake' if l['status']=='new' else 'Case Mgmt')}**")
            st.caption(f"{l['city']}  •  Next: start intake")
            c1, c2 = st.columns([0.5, 0.5])
            with c1:
                if st.button("View Record Summary", key=f"open_ws_{l['id']}"):
                    st.session_state["ws_selected_lead"] = l["id"]
                    st.experimental_rerun()
            with c2:
                if st.button("Client Record", key=f"open_full_{l['id']}"):
                    store.set_selected_lead(l["id"])
                    if hasattr(st, "switch_page"):
                        st.switch_page("pages/04_Client_Record.py")
                    else:
                        st.experimental_rerun()

with right:
    st.subheader("Case Overview")
    current = next((x for x in store.get_leads() if x["id"] == st.session_state.get("ws_selected_lead")), None)
    if not current:
        st.info("Select a lead from the queue to see details.")
    else:
        with st.container(border=True):
            st.markdown(f"**{current['name']} • {current['city']}**")
            st.caption(f"Stage: {'Intake' if current['status']=='new' else 'Case Mgmt'} • Priority: 2 • Budget: ${current['budget']:,}")
            pct = store.get_progress(current["id"])
            st.progress(pct, text="Intake progress")
            st.text_area("Quick note", placeholder="Add a quick note...", key=f"note_{current['id']}")
            st.selectbox("Care needs", ["Choose options","Assistance with ADLs","Memory care", "Skilled nursing"], index=0)
            st.markdown("### Decision support (last results)")
            with st.container(border=True):
                rec = current.get("ds_recommendation", "Assisted Living")
                est = current.get("ds_est_cost", 4500)
                st.markdown(f"**Recommended:** {rec}")
                st.markdown(f"**Estimated cost:** ${est:,.0f} / month")
            if st.button("Open full client record", key=f"open_full_summary_{current['id']}"):
                store.set_selected_lead(current['id'])
                if hasattr(st, 'switch_page'):
                    st.switch_page('pages/04_Client_Record.py')
                else:
                    st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)