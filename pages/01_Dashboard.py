# 01_Dashboard.py — Dashboard (defensive init)
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

st.title("Advisor Dashboard")

def badge(text, bg, fg):
    st.markdown(f"<span style='background:{bg};color:{fg};padding:2px 8px;border-radius:999px;font-size:11px;border:1px solid rgba(0,0,0,0.06)'>{text}</span>", unsafe_allow_html=True)

def kpi_card(title, value, sub=""):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(f"<div style='font-size:28px;font-weight:700'>{value}</div>", unsafe_allow_html=True)
        if sub: st.caption(sub)

leads = store.get_leads()
leads_today = [x for x in leads if x["created"] == date.today()]
assigned = [x for x in leads if x["assigned_to"]]
active_cases = [x for x in leads if x["status"] in ("new","in_progress")]

l1, l2, l3, l4 = st.columns([1,1,1,1.2])
with l1: kpi_card("New leads (today)", len(leads_today), "+ App and other sources")
with l2: kpi_card("Assigned leads", len(assigned))
with l3: kpi_card("Active cases", len(active_cases))
with l4: kpi_card("MTD vs goal", "$20,500 / $40,000", "51% of goal")

st.divider()
st.subheader("New Leads (Today)")

if not leads_today:
    st.write("No new leads today.")
else:
    for lead in leads_today[:5]:
        c1, c2, c3, c4, c5 = st.columns([0.35, 0.15, 0.18, 0.22, 0.10])
        with c1:
            st.markdown(f"**{lead['name']}**")
            st.caption(lead["city"])
        with c2:
            if lead["origin"] == "app":
                badge("App Lead", "#ecfdf5", "#065f46")
            elif lead["origin"] == "phone":
                badge("Phone", "#eff6ff", "#1d4ed8")
            else:
                badge(lead["origin"].title(), "#f3f4f6", "#374151")
        with c3:
            st.caption(f"{lead['preference']}" + (f" – est. ${lead['budget']:,}" if lead["budget"] else ""))
        with c4:
            st.caption(f"Timeline: {lead['timeline']}")
        with c5:
            if st.button("Open", key=f"open_{lead['id']}"):
                store.set_selected_lead(lead["id"])
                # switch_page may not exist on older versions
                if hasattr(st, "switch_page"):
                    st.switch_page("pages/04_Client_Record.py")
                else:
                    st.experimental_rerun()
