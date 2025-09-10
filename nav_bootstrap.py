
# nav_bootstrap.py — call boot() at top of visible pages to keep the sidebar clean
from ui_chrome import hide_pages

def boot():
    hide_pages([
        "00_Workflows",
        "06_Intake_Workflow",
        "07_Placement_Workflow",
        "08_Followup_Workflow",
    ])
