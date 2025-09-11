import streamlit as st
from datetime import datetime
from .intake_sla import summarize_intake, progress_percent, STAGES

def _fmt_dt(dt: datetime | None) -> str:
    if not dt:
        return "—"
    return dt.strftime("%Y-%m-%d %H:%M")

def intake_progress_ui(lead: dict, *, title: str = "Intake Progress"):
    if not lead:
        st.info("No client selected.")
        return

    st.subheader(title)
    pct = progress_percent(lead)
    st.progress(pct)

    summary = summarize_intake(lead)

    cols = st.columns(4)
    cols[0].markdown("<span style='color:#10b981'>●</span> Done", unsafe_allow_html=True)
    cols[1].markdown("<span style='color:#3b82f6'>●</span> Due", unsafe_allow_html=True)
    cols[2].markdown("<span style='color:#ef4444'>●</span> Late", unsafe_allow_html=True)
    cols[3].markdown("<span style='color:#6b7280'>●</span> Pending", unsafe_allow_html=True)

    st.write("")

    for s in STAGES:
        info = summary[s]
        label = info["label"]
        status = info["status"]
        done_at = info["completed_at"]
        due_at = info["due_at"]
        sla = info["sla"]

        color = {
            "done": "#10b981",
            "due": "#3b82f6",
            "late": "#ef4444",
            "pending": "#6b7280",
        }.get(status, "#6b7280")

        with st.container(border=True):
            c1, c2, c3 = st.columns([0.08, 0.62, 0.30])
            with c1:
                st.markdown(f"<span style='font-size:18px;color:{color}'>●</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"**{label}**", unsafe_allow_html=True)
                if sla:
                    st.caption(sla)
            with c3:
                if status == "done":
                    st.caption(f"Done: {_fmt_dt(done_at)}")
                elif status in ("due", "late"):
                    st.caption(f"Due: {_fmt_dt(due_at)}")
                else:
                    st.caption("—")
