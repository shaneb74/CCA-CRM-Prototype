
import streamlit as st
from typing import Optional, Callable

def inject_css():
    st.markdown('''
    <style>
      .tile { border:1px solid #e6e6e6;border-radius:12px;padding:14px 16px;background:#fff;
              box-shadow:0 1px 2px rgba(0,0,0,0.04);margin-bottom:12px; }
      .kpi { border-radius:12px;border:1px solid #e6e6e6;background:#fff;padding:12px 16px;margin-bottom:8px; min-height:92px; display:flex; flex-direction:column; justify-content:space-between; }
      .kpi .label { color:#57606a;font-size:0.85rem; } .kpi .value { font-weight:700;font-size:1.6rem;line-height:1.2; }
      .note { border-left:4px solid #228be6;background:#f0f7ff;padding:10px 12px;border-radius:6px;margin:8px 0; }
      .pill { display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;color:#fff;margin-left:8px; }
      .pill.comp { background:#1c7ed6; } .pill.fin { background:#2f9e44; } .pill.gen { background:#868e96; }
      .banner-text { font-size: 0.95rem; }
      .chips { display:flex; gap:8px; flex-wrap:wrap; margin:6px 0 14px 0;}
      .chip { border:1px solid #e6e6e6; background:#fff; border-radius:999px; padding:4px 10px; font-size:12px; color:#334155;}
      .muted { color:#6b7280; font-size:0.9rem; }
      .ctx-panel { border-left:1px solid #e6e6e6; padding-left:16px; }
      .small { font-size: 0.9rem; }

      /* --- KPI band (sticky at-a-glance) --- */
      .kpi-band {
        position: sticky; top: 52px; z-index: 5;
        background: #ffffff;
        border: 1px solid #e9edf3;
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(16,24,40,0.06);
        padding: 14px 16px;
        margin-bottom: 18px;
      }
      .kpi-title { font-size: 13px; color: #6b7280; letter-spacing: .2px; margin: 0 0 6px 0; }
      .kpi-value { font-size: 28px; line-height: 1.1; font-weight: 700; color: #0f172a; margin: 0; }
      .kpi-sub { font-size: 12px; color: #6b7280; }
      .kpi-delta {
        display: inline-block; font-size: 12px; padding: 2px 8px; border-radius: 12px; margin-left: 8px; border: 1px solid;
      }
      .kpi-delta.pos { color: #027a48; border-color: #a7f3d0; background: #ecfdf5; }
      .kpi-delta.neg { color: #b42318; border-color: #fecaca; background: #fef2f2; }
      .kpi-delta.neu { color: #334155; border-color: #e2e8f0; background: #f8fafc; }
      .kpi-divider { height: 1px; background: #eef2f7; margin: 8px 0; display: none; }
      @media (max-width: 900px) { .kpi-divider { display:block; } }
    </style>
    ''', unsafe_allow_html=True)

def section(title:str):
    st.subheader(title); st.write("")

def kpi(label:str, value:str, help_text:str=""):
    st.markdown(f"<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div><div class='muted'>{help_text}</div></div>", unsafe_allow_html=True)

def alert(text:str):
    st.markdown(f"<div class='note banner-text'>{text}</div>", unsafe_allow_html=True)

def tile(title:str, body:str=''):
    st.markdown(f"<div class='tile'><strong>{title}</strong><br/><span style='color:#57606a'>{body}</span></div>", unsafe_allow_html=True)

def progress(label:str, pct:float):
    st.write(label); st.progress(int(max(0,min(100,pct))))

def chips(items):
    html = "<div class='chips'>" + "".join([f"<span class='chip'>{t}</span>" for t in items]) + "</div>"
    st.markdown(html, unsafe_allow_html=True)

# --- New helpers for At-a-glance band ---
def kpi_pill(title: str, value: str, subtitle: Optional[str] = None,
             delta: Optional[str] = None, intent: str = "neu"):
    st.markdown(f"<div class='kpi-title'>{title}</div>", unsafe_allow_html=True)
    c_val, c_badge = st.columns([1, 1])
    with c_val:
        st.markdown(f"<div class='kpi-value'>{value}</div>", unsafe_allow_html=True)
    with c_badge:
        if delta is not None:
            st.markdown(
                f"<div class='kpi-delta {intent}' style='float:right'>{delta}</div>",
                unsafe_allow_html=True
            )
    if subtitle:
        st.markdown(f"<div class='kpi-sub'>{subtitle}</div>", unsafe_allow_html=True)

def kpi_band(render_fn: Callable[[], None]):
    st.markdown("<div class='kpi-band'>", unsafe_allow_html=True)
    render_fn()
    st.markdown("</div>", unsafe_allow_html=True)
