
import streamlit as st

def inject_css():
    st.markdown('''
    <style>
      :root { --card-border:#e6e6e6; --muted:#57606a; --bg:#ffffff; }
      .tile { border:1px solid var(--card-border); border-radius:12px; padding:14px 16px; background:#fff;
              box-shadow:0 1px 2px rgba(0,0,0,0.04); margin-bottom:12px; }
      .kpi { border-radius:12px; border:1px solid var(--card-border); background:#fff; padding:12px 16px;
             margin-bottom:8px; min-height:92px; display:flex; flex-direction:column; justify-content:space-between; }
      .kpi .label { color:var(--muted); font-size:0.85rem; }
      .kpi .value { font-weight:700; font-size:1.6rem; line-height:1.2; }
      .note { border-left:4px solid #228be6; background:#f0f7ff; padding:10px 12px; border-radius:6px; margin:8px 0; }
      .sticky { position: sticky; top: 0; z-index: 20; background: #f8fafc; padding-top: 6px; padding-bottom: 6px; }
      .pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; color:#fff; margin-left:8px; }
      .pill.comp { background:#1c7ed6; } .pill.fin { background:#2f9e44; } .pill.gen { background:#868e96; }
      .banner-text { font-size: 0.95rem; }
      .banner { background:#f0f7ff; border-left:4px solid #228be6; padding:8px 12px; border-radius:6px; margin-bottom:8px; }
      .card { border:1px solid var(--card-border); border-radius:12px; background:var(--bg); padding:10px 12px; margin-bottom:10px; }
      .mini { color:var(--muted); font-size:0.9rem; }
      .tag { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; color:#fff; }
      .tag.pri { background:#d9480f } .tag.sec{ background:#1c7ed6 } .tag.ok{ background:#2f9e44 }
    </style>
    ''', unsafe_allow_html=True)

def section(title:str):
    st.subheader(title); st.write("")

def kpi(label:str, value:str, help_text:str=""):
    st.markdown(f"<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div><div>{help_text}</div></div>", unsafe_allow_html=True)

def alert(text:str):
    st.markdown(f"<div class='note banner-text'>{text}</div>", unsafe_allow_html=True)

def tile(title:str, body:str=''):
    st.markdown(f"<div class='tile'><strong>{title}</strong><br/><span style='color:#57606a'>{body}</span></div>", unsafe_allow_html=True)

def progress(label:str, pct:float):
    st.write(label); st.progress(int(max(0,min(100,pct))))

# New helpers used by Advisor Workspace
def banner(text:str):
    st.markdown(f"<div class='banner'>{text}</div>", unsafe_allow_html=True)

def card(title:str, body:str):
    st.markdown(f"<div class='card'><strong>{title}</strong><div class='mini'>{body}</div></div>", unsafe_allow_html=True)

def tag(text:str, kind:str='sec'):
    st.markdown(f"<span class='tag {kind}'>{text}</span>", unsafe_allow_html=True)
