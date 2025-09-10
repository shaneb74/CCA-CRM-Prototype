
READ ME — Keep the sidebar clean and use contextual links for workflows

1) Copy files from this zip into your repo:
   - ui_chrome.py  (repo root)
   - nav_bootstrap.py (repo root)
   - pages/00_Workflows.py
   - pages/06_Intake_Workflow.py
   - pages/07_Placement_Workflow.py
   - pages/08_Followup_Workflow.py

2) In EACH visible page (right after st.set_page_config(...)):
       from nav_bootstrap import boot
       boot()

   Visible pages are:
       01_Dashboard.py
       02_Advisor_Workspace.py
       03_Supervisor_Workspace.py
       04_Client_Record.py
       05_Notifications.py

3) File names (order the sidebar):
       01_Dashboard.py
       02_Advisor_Workspace.py
       03_Supervisor_Workspace.py
       04_Client_Record.py
       05_Notifications.py
       00_Workflows.py              (hidden hub, still routable)
       06_Intake_Workflow.py        (hidden)
       07_Placement_Workflow.py     (hidden)
       08_Followup_Workflow.py      (hidden)

4) Access paths (with sidebar entries hidden):
   - Dashboard “Advisor Workflows” section: page_link to Intake/Placement/Follow-up
   - Client Record header: a “Workflows →” page_link (sets context if needed)
   - Advisor Workspace Case Overview: optional same link

5) If you ever want to show the hub in the sidebar:
   - Remove the hide call in pages/00_Workflows.py
   - Or simply add it to the numbered set as 05_Workflows.py (not recommended)
