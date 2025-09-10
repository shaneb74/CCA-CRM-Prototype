
# nav_bootstrap.py — import and call boot() at the top of *visible* pages
from ui_chrome import hide_pages

def boot():
    # Hide anything unnecessary from sidebar across visible pages
    hide_pages([
        "00_Workflows",
        "06_Intake_Workflow",
        "07_Placement_Workflow",
        "08_Followup_Workflow"
    ])
