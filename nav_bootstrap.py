
# nav_bootstrap.py — call boot() after set_page_config on visible pages
from ui_chrome import hide_pages

def boot():
    hide_pages([
        "00_Workflows",
        "06_Intake_Workflow",
        "07_Placement_Workflow",
        "08_Followup_Workflow",
    ])
