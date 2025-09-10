
README — Full pages restore

1) Unzip into your repo so files land here:
   ui_chrome.py
   nav_bootstrap.py
   ui_sections.py
   pages/00_Workflows.py
   pages/01_Dashboard.py
   pages/02_Advisor_Workspace.py
   pages/03_Notifications.py
   pages/04_Client_Record.py
   pages/05_Supervisor_Workspace.py
   pages/06_Intake_Workflow.py
   pages/07_Placement_Workflow.py
   pages/08_Followup_Workflow.py

2) Sidebar order is controlled by filenames (01..05).

3) Workflows are hidden from the sidebar by:
   - self-hiding CSS in each workflow page
   - and the boot() call below for belt-and-suspenders.

4) In each visible page (01..05) we already added:
       from nav_bootstrap import boot; boot()

5) You still need your existing store.py (not included here).
