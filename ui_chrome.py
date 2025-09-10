# ui_chrome.py — robustly hide workflow pages from the sidebar
import streamlit as st
from textwrap import dedent

# Sidebar labels exactly as they appear
HIDE_TITLES = [
    "Workflows",
    "Intake Workflow",
    "Placement Workflow",
    "Followup Workflow",
]

# Optional href fragments (works in many setups; harmless otherwise)
HIDE_HREFS = [
    "/00_Workflows",
    "/06_Intake_Workflow",
    "/07_Placement_Workflow",
    "/08_Followup_Workflow",
]

def hide_default():
    # CSS-by-href fallback
    if HIDE_HREFS:
        selectors = ",".join([f'section[data-testid="stSidebar"] a[href*="{frag}"]'
                               for frag in HIDE_HREFS])
        st.markdown(f"<style>{selectors}{{display:none!important;}}</style>", unsafe_allow_html=True)

    # JS-by-label, resilient to URL changes and rerenders
    js = dedent(f"""
    <script>
    const HIDE_TITLES = {HIDE_TITLES!r};
    const HIDE_HREFS  = {HIDE_HREFS!r};
    function hideItems() {{
      const side = document.querySelector('section[data-testid="stSidebar"]');
      if (!side) return;
      const links = side.querySelectorAll('a[href]');
      links.forEach(a => {{
        const txt = (a.textContent || '').trim();
        const href = a.getAttribute('href') || '';
        const hitTitle = HIDE_TITLES.includes(txt);
        const hitHref  = HIDE_HREFS.some(f => href.includes(f));
        if (hitTitle || hitHref) {{
          (a.parentElement || a).style.display = 'none';
        }}
      }});
    }}
    hideItems();
    const obs = new MutationObserver(hideItems);
    obs.observe(document.body, {{ subtree: true, childList: true }});
    </script>
    """)
    st.markdown(js, unsafe_allow_html=True)