
README — Hide Workflow Pages from Sidebar

This bundle includes:
- ui_chrome.py with hide_default()
- Updated visible pages (01–05) that already import & call hide_default()

How to apply:
1. Merge ui_chrome.py into your repo root (replace existing).
2. For each visible page (01–05), integrate the top 3 lines into your actual code:
   from ui_chrome import hide_default
   hide_default()
   (make sure it's right after st.set_page_config)
3. Replace the placeholder st.title(...) sections with your actual page code.

Result:
Workflow pages (00_Workflows, 06_Intake_Workflow, 07_Placement_Workflow, 08_Followup_Workflow)
will never appear in the sidebar, but remain routable via page_link / switch_page.
