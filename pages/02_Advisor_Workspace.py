# 02_Advisor_Workspace.py — Work Queue (defensive init + control fallback)
import streamlit as st
import store
store.init()

def segmented(label, options, default):
    # Use segmented_control if available; otherwise fall back to radio
    if hasattr(st, "segmented_control"):
        return st.segmented_control(label, options=options, default=default)
    else:
        return st.radio(label, options, index=options.index(default), horizontal=True)


from datetime import date

st.title("Advisor Workspace")

def chip(text):
    st.markdown(f"<span style='background:#f3f4f6;color:#111;padding:3px 10px;border-radius:999px;font-size:12px;border:1px solid #e5e7eb'>{text}</span>", unsafe_allow_html=True)

left, right = st.columns([0.7, 0.3])
with left:
    origin = segmented("Origin", ["All","App","Phone","Hospital"], "All")
with right:
    due_filter = segmented("Due", ["All","Today","Upcoming"], "All")

def origin_match(o):
    if origin == "All": return True
    mapping = {"App":"app", "Phone":"phone", "Hospital":"hospital"}
    return o == mapping[origin]

def due_match(d):
    if due_filter == "All": return True
    if due_filter == "Today": return d == date.today()
    return d > date.today()

tasks = [t for t in store.get_tasks(active_only=True) if origin_match(t["origin"]) and due_match(t["due"])]

if not tasks:
    st.write("Nothing in your queue.")
else:
    leads = {l["id"]: l for l in store.get_leads()}
    for t in tasks:
        c1, c2, c3, c4 = st.columns([0.50, 0.15, 0.20, 0.15])
        lead = leads.get(t["lead_id"])
        with c1:
            st.markdown(f"**{t['title']}**")
            if lead: st.caption(f"{lead['name']} • {lead['city']}")
        with c2:
            chip("App Lead" if t["origin"] == "app" else t["origin"].title())
        with c3:
            st.caption(f"Due: {t['due'].isoformat()}  •  Priority: {t['priority']}")
        with c4:
            colb1, colb2 = st.columns([0.6,0.4])
            with colb1:
                if st.button("Open", key=f"open_{t['id']}"):
                    store.set_selected_lead(t["lead_id"])
                    if hasattr(st, "switch_page"):
                        st.switch_page("pages/04_Client_Record.py")
                    else:
                        st.experimental_rerun()
            with colb2:
                if st.button("✓", key=f"done_{t['id']}", help="Complete"):
                    store.complete_task(t["id"])
                    st.experimental_rerun()
