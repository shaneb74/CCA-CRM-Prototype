
PATCH INSTRUCTIONS (nav cleanup + hidden hub)

Goal:
- Keep only these visible (in this order): 
  Dashboard, Advisor Workspace, Notifications, Client Record, Supervisor Workspace
- Hide the hub + guided workflow pages from the left sidebar.

Files in this bundle:
- ui_chrome.py
- pages/00_Workflows.py   (fixed; hidden from sidebar)
- nav_bootstrap.py

Step 1: Copy files
- Place ui_chrome.py in repo root.
- Place pages/00_Workflows.py in your pages/ folder (overwriting your hub).
- Place nav_bootstrap.py in repo root.

Step 2: Add 2 lines to EACH visible page:
   - 01_Dashboard.py
   - 02_Advisor_Workspace.py
   - 03_Notifications.py
   - 04_Client_Record.py
   - 05_Supervisor_Workspace.py

Add these lines immediately AFTER st.set_page_config(...):
    from nav_bootstrap import boot
    boot()

Step 3: File naming for order (ensure these exact filenames):
   01_Dashboard.py
   02_Advisor_Workspace.py
   03_Notifications.py
   04_Client_Record.py
   05_Supervisor_Workspace.py
   06_Intake_Workflow.py        (hidden)
   07_Placement_Workflow.py     (hidden)
   08_Followup_Workflow.py      (hidden)
   00_Workflows.py              (hidden hub, still routable)

Notes:
- We hide via CSS selectors. Routes still work, so page_link/switch_page keep functioning.
- st.set_page_config must be the first Streamlit call on each page.
