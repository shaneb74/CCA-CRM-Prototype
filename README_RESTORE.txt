
CLEAN RESTORE (no edits to your pages)

- This is your Archive.zip, plus:
  * ui_chrome.py
  * ui_sections.py
  * pages/00_Workflows.py (hidden hub)
  * pages/06_Intake_Workflow.py (hidden)
  * pages/07_Placement_Workflow.py (hidden)
  * pages/08_Followup_Workflow.py (hidden)

- Your existing pages are untouched.
- To hide workflows proactively from the sidebar on all pages, add to each visible page (right after st.set_page_config):
    from ui_chrome import hide_default
    hide_default()
