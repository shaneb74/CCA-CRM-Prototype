
import streamlit as st
from contextlib import contextmanager

def inject_css():
    st.markdown(
        """
        <style>
          .cca-card {
            background: #ffffff;
            border: 1px solid rgba(0,0,0,0.07);
            border-radius: 12px;
            padding: 16px 18px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            margin-bottom: 12px;
          }
          .cca-kpi-band {
            border: 1px solid rgba(0,0,0,0.07);
            border-radius: 14px;
            padding: 18px;
            background: #fafbff;
            margin-bottom: 16px;
          }
          .cca-kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
          }
          .cca-kpi h4 {
            font-size: 0.9rem;
            color: #51607a;
            margin: 0 0 6px 0;
            font-weight: 600;
          }
          .cca-kpi .val {
            font-size: 2rem;
            line-height: 2.2rem;
            font-weight: 800;
            color: #0f172a;
          }
          .pill {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 12px;
            border: 1px solid rgba(0,0,0,0.08);
            background: #f6f7fb;
            color: #334155;
            margin-left: 8px;
            vertical-align: middle;
          }
          .pill.green { background: #eaf7ee; color: #166534; border-color: #bbdec5; }
          .pill.red { background: #fdecec; color: #991b1b; border-color: #f3b4b4; }
          .pill.gray { background: #f1f5f9; color: #334155; border-color: #e2e8f0;}
          .banner {
            background: #eef5ff;
            border: 1px solid #dbeafe;
            padding: 12px 14px;
            border-radius: 8px;
            color: #0f172a;
            margin-bottom: 8px;
          }
          .x-right {
            float: right;
            color: #475569;
            cursor: pointer;
          }
        </style>
        """,
        unsafe_allow_html=True
    )

@contextmanager
def card(title=None):
    st.markdown('<div class="cca-card">', unsafe_allow_html=True)
    if title:
        st.subheader(title)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)

@contextmanager
def kpi_band(title="At a glance"):
    st.markdown('<div class="cca-kpi-band">', unsafe_allow_html=True)
    if title:
        st.markdown(f"### {title}")
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)

def kpi(label, value, pill_text=None, pill_color="gray"):
    st.markdown('<div class="cca-kpi">', unsafe_allow_html=True)
    st.markdown(f"<h4>{label}</h4>", unsafe_allow_html=True)
    st.markdown(f'<div class="val">{value}</div>', unsafe_allow_html=True)
    if pill_text:
        pc = pill_color if pill_color in {"green","red","gray"} else "gray"
        st.markdown(f'<span class="pill {pc}">{pill_text}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def chips(items):
    if not items:
        return
    st.markdown(" ".join([f'<span class="pill gray">{t}</span>' for t in items]), unsafe_allow_html=True)

@contextmanager
def tile(title=None, subtitle=None):
    with card(None):
        if title:
            st.markdown(f"**{title}**" + (f" — {subtitle}" if subtitle else ""))
        yield

def banner(text, category="info", show_close=False, key=None):
    st.markdown('<div class="banner">', unsafe_allow_html=True)
    if show_close:
        st.markdown('<span class="x-right">✕</span>', unsafe_allow_html=True)
    st.write(text)
    st.markdown("</div>", unsafe_allow_html=True)

def pills_row(pairs):
    html = " ".join([f'<span class="pill {c if c in {"green","red","gray"} else "gray"}">{t}</span>' for t,c in pairs])
    st.markdown(html, unsafe_allow_html=True)
