
import streamlit as st

def inject_css():
    st.markdown('''
    <style>
      :root {
        --card-border:#e6e6e6;
        --muted:#57606a;
        --bg:#ffffff;
      }
      .sticky { position: sticky; top: 0; z-index: 30; background: #f8fafc; padding: 8px 0 10px 0; }
      .kpi { border:1px solid var(--card-border); border-radius:12px; background:#fff; padding:10px 12px; min-height:84px; display:flex; flex-direction:column; justify-content:space-between; }
      .kpi .label { color:var(--muted); font-size:0.82rem }
      .kpi .value { font-weight:700; font-size:1.4rem; line-height:1.2 }
      .banner { background:#f0f7ff; border-left:4px solid #228be6; padding:8px 12px; border-radius:6px; margin-bottom:8px }
      .tag { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; color:#fff; }
      .tag.pri { background:#d9480f } .tag.sec{ background:#1c7ed6 } .tag.ok{ background:#2f9e44 }
      .card { border:1px solid var(--card-border); border-radius:12px; background:var(--bg); padding:10px 12px; margin-bottom:10px; }
      .board { display:grid; grid-template-columns: repeat(4, minmax(200px, 1fr)); gap:12px; }
      .col { border:1px dashed #e6e6e6; border-radius:12px; padding:8px; background:#fcfcfd; }
      .col h4 { margin:4px 0 8px 0; font-size:1.0rem }
      .mini { color:var(--muted); font-size:0.9rem }
      .pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; color:#fff }
      .pill.comp{ background:#1c7ed6 } .pill.fin{ background:#2f9e44 } .pill.gen{ background:#868e96 }
    </style>
    ''', unsafe_allow_html=True)

def kpi(label, value, help_text=""):
    st.markdown(f"<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div><div class='mini'>{help_text}</div></div>", unsafe_allow_html=True)

def banner(text):
    st.markdown(f"<div class='banner'>{text}</div>", unsafe_allow_html=True)

def card(title, body):
    st.markdown(f"<div class='card'><strong>{title}</strong><div class='mini'>{body}</div></div>", unsafe_allow_html=True)

def tag(text, kind="sec"):
    st.markdown(f"<span class='tag {kind}'>{text}</span>", unsafe_allow_html=True)
