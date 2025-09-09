
import streamlit as st

def inject_css():
    st.markdown('''
    <style>
      .tile { border:1px solid #e6e6e6;border-radius:12px;padding:14px 16px;background:#fff;
              box-shadow:0 1px 2px rgba(0,0,0,0.04);margin-bottom:12px; }
      .tile h4 { margin:0 0 6px 0; font-size:1.0rem; }
      .tile p { margin:0; color:#57606a; font-size:0.92rem; }
      .kpi { border-radius:12px;border:1px solid #e6e6e6;background:#fff;padding:12px 16px; }
      .kpi .label { color:#57606a;font-size:0.85rem; } .kpi .value { font-weight:700;font-size:1.6rem;line-height:1.2; }
      .note { border-left:4px solid #228be6;background:#f0f7ff;padding:10px 12px;border-radius:6px;margin-bottom:10px; }
      .pill { display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;color:#fff;margin-left:8px; }
      .pill.ok { background:#2f9e44; } .pill.warn { background:#d9480f; } .pill.due { background:#1c7ed6; } .pill.over { background:#e03131; }
      .stage { font-weight:600; margin-top:6px; margin-bottom:2px; }
    </style>
    ''', unsafe_allow_html=True)

def section(title:str):
    st.subheader(title); st.write("")

def kpi(label:str, value:str, help_text:str=""):
    st.markdown(f"<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div><div>{help_text}</div></div>", unsafe_allow_html=True)

def pill(text:str, tone:str="ok"):
    st.markdown(f"<span class='pill {tone}'>{text}</span>", unsafe_allow_html=True)

def tile(title:str, body:str='', link:str=None, link_label:str='Open'):
    st.markdown(f"<div class='tile'><h4>{title}</h4><p>{body}</p></div>", unsafe_allow_html=True)
    if link:
        st.page_link(link, label=link_label)

def alert(text:str):
    st.markdown(f"<div class='note'>{text}</div>", unsafe_allow_html=True)

def progress(label:str, pct:float):
    st.write(label); st.progress(int(max(0,min(100,pct))))
