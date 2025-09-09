
import streamlit as st
from typing import Callable, Optional

def inject_css():
    st.markdown('''
    <style>
      .tile { border:1px solid #e6e6e6;border-radius:12px;padding:14px 16px;background:#fff;
              box-shadow:0 1px 2px rgba(0,0,0,0.04);margin-bottom:12px; }
      .muted { color:#6b7280; font-size:0.9rem; }
      .kpi-title { font-size: 13px; color: #64748b; letter-spacing: .2px; margin: 0 0 6px 0; }
      .kpi-value { font-size: 28px; line-height: 1.1; font-weight: 700; color: #0f172a; margin: 0; }
      .kpi-sub { font-size: 12px; color: #64748b; }
      .kpi-delta { display: inline-block; font-size: 12px; padding: 2px 8px; border-radius: 12px; margin-left: 8px; border: 1px solid; }
      .kpi-delta.pos { color: #027a48; border-color: #a7f3d0; background: #ecfdf5; }
      .kpi-delta.neg { color: #b42318; border-color: #fecaca; background: #fef2f2; }
      .kpi-delta.neu { color: #334155; border-color: #e2e8f0; background: #f8fafc; }

      /* New At-a-glance card */
      .kpi-wrap {
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 14px 18px 8px 18px;
        background: linear-gradient(180deg,#ffffff 0%, #f9fafb 100%);
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        margin-bottom: 8px;
      }
      .kpi-wrap .hdr {
        display:flex; align-items:center; justify-content:space-between;
        padding-bottom: 6px; margin-bottom: 10px; border-bottom: 1px dashed #e5e7eb;
      }
      .kpi-wrap .hdr .title {
        font-weight: 600; color:#0f172a; letter-spacing:.2px;
      }
      .kpi-pill { padding: 4px 8px; font-size: 12px; border:1px solid #e2e8f0; border-radius:999px; color:#334155; background:#fff; }
    </style>
    ''', unsafe_allow_html=True)

def section(title:str): st.subheader(title); st.write("")

def tile(title:str, body:str=''):
    st.markdown(f"<div class='tile'><strong>{title}</strong><br/><span class='muted'>{body}</span></div>", unsafe_allow_html=True)

def progress(label:str, pct:float): st.write(label); st.progress(int(max(0,min(100,pct))))

def at_a_glance(render: Callable[[], None], pills: Optional[list[str]] = None):
    st.markdown("<div class='kpi-wrap'>", unsafe_allow_html=True)
    left, right = st.columns([5,2])
    with left:
        st.markdown("<div class='hdr'><div class='title'>At a glance</div></div>", unsafe_allow_html=True)
    with right:
        if pills:
            pill_html = " ".join([f"<span class='kpi-pill'>{p}</span>" for p in pills])
            st.markdown(f"<div style='text-align:right' class='hdr'><div>{pill_html}</div></div>", unsafe_allow_html=True)
    # row of four KPIs
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    render_cols = [c1,c2,c3,c4]
    render(*render_cols)  # render function receives the 4 columns
    st.markdown("</div>", unsafe_allow_html=True)

def kpi_block(col, title:str, value:str, subtitle:str="", delta:Optional[str]=None, intent:str="neu"):
    with col:
        st.markdown(f"<div class='kpi-title'>{title}</div>", unsafe_allow_html=True)
        c_val, c_badge = st.columns([1,1])
        with c_val:
            st.markdown(f"<div class='kpi-value'>{value}</div>", unsafe_allow_html=True)
        with c_badge:
            if delta:
                st.markdown(f"<div class='kpi-delta {intent}' style='float:right'>{delta}</div>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<div class='kpi-sub'>{subtitle}</div>", unsafe_allow_html=True)
