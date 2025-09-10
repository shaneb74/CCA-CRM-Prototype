# ui_chrome.py — robustly hide workflow pages from the sidebar
import streamlit as st
from textwrap import dedent

# Titles as they appear in the sidebar (not file names)
HIDE_TITLES = [
    "Workflows",
    "Intake Workflow",
    "Placement Workflow",
    "Followup Workflow",
]

# Optional href fragments as a fallback (covers 00_/06_/07_/08_ filenames)
HIDE_HREFS = [
    "/00_Workflows",
    "/06_Intake_Workflow",
    "/07_Placement_Workflow",
    "/08_Followup_Workflow",
]

def hide_default():
    if not (HIDE_TITLES or HIDE_HREFS):
        return

    # 1) CSS fallback: hide by href fragment if present
    if HIDE_HREFS:
        selectors = ",".join([f'section[data-testid="stSidebar"] a[href*="{frag}"]'
                               for frag in HIDE_HREFS])
        st.markdown(f"<style>{selectors}{{display:none!important;}}</style>", unsafe_allow_html=True)

    # 2) JS: hide by link text (works regardless of href structure)
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
          // Hide the whole nav row (anchor or its parent container)
          (a.parentElement || a).style.display = 'none';
        }}
      }});
    }}
    // Run now and again after rerenders
    hideItems();
    const obs = new MutationObserver(hideItems);
    const root = document.body;
    if (root) obs.observe(root, {{ subtree: true, childList: true }});
    </script>
    """)
    st.markdown(js, unsafe_allow_html=True)
