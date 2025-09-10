# 02_Advisor_Workspace.py — split-pane list + inline summary, with Open button
import streamlit as st, store
from datetime import date, timedelta
store.init()

def segmented(label, options, default):
    if hasattr(st, "segmented_control"):
        return st.segmented_control(label, options=options, default=default)
    return st.radio(label, options, index=options.index(default), horizontal=True)

def badge(text, bg="#f3f4f6", fg="#374151"):
    st.markdown(f"<span class='badge' style='background:{bg};color:{fg}'> {text} </span>", unsafe_allow_html=True)

def kpi_card(title, value, sub_html=""):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(f"<div class='num'>{value}</div>", unsafe_allow_html=True)
        if sub_html:
            st.markdown(sub_html, unsafe_allow_html=True)


st.title("Advisor Workspace")
st.markdown("""<style>
  .page {max-width:1200px;margin:0 auto}
  .kpi .num {font-size:28px;font-weight:700;color:#111827}
  .badge {display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid rgba(0,0,0,0.06)}
  .badge.green {background:#ecfdf5;color:#065f46}
  .badge.yellow {background:#fffbeb;color:#92400e}
  .rowcard {border:1px solid #e5e7eb;border-radius:14px;padding:12px;background:#fff}
  .task-title{font-weight:600;color:#111827;margin-bottom:2px}
  .task-sub{font-size:12px;color:#6b7280}
  .lead-card{border:1px solid #e5e7eb;border-radius:14px;padding:12px;background:#fff}
  .lead-card:hover{box-shadow:0 0 0 2px #e5e7eb}
  .summary-card{border:1px solid #e5e7eb;border-radius:14px;padding:16px;background:#fff}
  .dim{color:#6b7280}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="page">', unsafe_allow_html=True)

# Filters
f1, f2 = st.columns([0.6, 0.4])
with f1:
    origin = segmented("Filter", ["All leads","App","Phone","Hospital"], "All leads")
with f2:
    stage = segmented("Stage", ["All","Lead Received","Intake","Case Mgmt"], "All")

def origin_ok(o):
    if origin == "All leads": return True
    return o == {"App":"app","Phone":"phone","Hospital":"hospital"}[origin]

leads = [l for l in store.get_leads() if origin_ok(l["origin"])]

# Selection handling
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
            st.text_area("Quick note", placeholder="Add a quick note...", key=f"note_{current['id']}")
            st.progress(0.35, text="Intake progress")
            st.selectbox("Care needs", ["Choose options","Assistance with ADLs","Memory care", "Skilled nursing"], index=0)
            st.markdown("### Decision support (last results)")
            with st.container(border=True):
                st.markdown("**Recommended:** Assisted Living")
                st.markdown("**Estimated cost:** $4,500 / month")
            st.button("Open full client record", key=f"open_full_summary_{current['id']}", on_click=lambda: store.set_selected_lead(current['id']))

st.markdown('</div>', unsafe_allow_html=True)
