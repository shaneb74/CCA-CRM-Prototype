# ui_chrome.py
import streamlit as st

# call this at the top of every page once (you already do this from store/app)
def hide_default():
    st.markdown(
        """
        <style>
        /* keep sidebar tidy */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {padding-top: .5rem;}
        /* --- HIDE specific pages in the sidebar nav --- */

        /* List every route slug part that should be hidden.
           We match contains() because Streamlit builds hrefs like /<app>/?page=pages%2F06_Intake_Workflow.py
           These cover both the hub and the three child workflow pages. */

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="00_Workflows.py"] {display:none !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="06_Intake_Workflow.py"] {display:none !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="07_Placement_Workflow.py"] {display:none !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="08_Followup_Workflow.py"] {display:none !important;}

        /* Fallback: also hide by title slugs in case Streamlit changes the query-path */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="Workflows"] {display:none !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="Intake_Workflow"] {display:none !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="Placement_Workflow"] {display:none !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="Followup_Workflow"] {display:none !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )
