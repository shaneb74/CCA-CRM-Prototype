
import streamlit as st

# Minimal, battle-tested helpers (no emojis, no external deps)

def inject_css():
    st.markdown(
        """
        <style>
        /* Global tweak */
        .block-container{padding-top:2rem;max-width:1200px;}
        /* At-a-glance panel */
        .glance-card {
            border:1px solid #e6e6e6;
            border-radius:14px;
            padding:18px 20px 8px 20px;
            background:#fafafa;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }
        .glance-title{font-weight:700;font-size:1.1rem;margin-bottom:.35rem;}
        .kpi {
            display:flex;flex-direction:column;gap:.25rem;
            min-width: 200px;
        }
        .kpi-label { color:#666; font-size:.90rem; }
        .kpi-value { font-size:1.6rem; font-weight:800; letter-spacing:.3px;}
        .pill {
            display:inline-block; padding:2px 8px; border-radius:999px;
            font-size:.75rem; border:1px solid;
        }
        .pill-good { color:#2c7a4b; border-color:#c6f6d5; background:#f0fff4;}
        .pill-warn { color:#975a16; border-color:#fbd38d; background:#fffbeb;}
        .pill-bad  { color:#9b2c2c; border-color:#fed7d7; background:#fff5f5;}
        .note {
            background:#eef6ff; border:1px solid #dbeafe; border-radius:10px;
            padding:10px 12px; margin-bottom:8px;
        }
        .note X {float:right}
        .card {
            border:1px solid #eee; border-radius:12px; padding:14px 16px; background:#fff;
        }
        .small-muted {color:#6b7280; font-size:.85rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def chips(items):
    """Render a row of tiny info chips (dicts with 'label' keys)."""
    st.markdown(
        " ".join([f"<span class='pill pill-good'>{st.html.escape(i['label']) if hasattr(st, 'html') else i['label']}</span>" for i in items]),
        unsafe_allow_html=True
    )

def tile(title:str, body:str=""):
    st.markdown(f"<div class='card'><div style='font-weight:700'>{title}</div><div class='small-muted'>{body}</div></div>", unsafe_allow_html=True)
