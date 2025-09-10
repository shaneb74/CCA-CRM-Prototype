
# quick_patch.py — add apply_chrome() safely to pages, remove raw set_page_config
import re, sys
from pathlib import Path

TITLE_MAP = {
    "01_Dashboard.py": ("Advisor Dashboard", "📊"),
    "02_Advisor_Workspace.py": ("Advisor Workspace", "🧑‍💼"),
    "03_Notifications.py": ("Notifications", "🔔"),
    "04_Client_Record.py": ("Case Overview", "📄"),
    "05_Supervisor_Workspace.py": ("Supervisor Workspace", "🧭"),
    "20_Entity_Management.py": ("Entity Management", "🧩"),
    "88_Workflows_Section.py": ("Workflows Section", "🧱"),
    "89_Workflows.py": ("Workflows", "🧱"),
    "90_Intake_Workflow.py": ("Intake Workflow", "📝"),
    "91_Placement_Workflow.py": ("Placement Workflow", "📍"),
    "92_Followup_Workflow.py": ("Follow-up Workflow", "✅"),
}

def guess_title(fname: str):
    if fname in TITLE_MAP:
        return TITLE_MAP[fname]
    name = Path(fname).stem
    name = re.sub(r"^\d+_", "", name).replace("_", " ").strip().title()
    return (name or "App", "📋")

def ensure_apply_chrome(text: str, title: str, icon: str) -> str:
    if "from ui_chrome import apply_chrome" not in text:
        text = "from ui_chrome import apply_chrome\n" + text
    lines = text.splitlines()
    insert_at = 0
    for i, ln in enumerate(lines[:40]):
        if ln.strip().startswith(("import ", "from ")):
            insert_at = i + 1
    call = f"apply_chrome({title!r}, {icon!r})"
    if call not in text:
        lines.insert(insert_at, call)
    return "\n".join(lines)

def remove_raw_set_page_config(text: str) -> str:
    pattern = re.compile(r"^\s*st\.set_page_config\([^\n]*\)\s*$", re.MULTILINE)
    return pattern.sub(lambda m: "# " + m.group(0), text)

def patch_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    orig = src
    title, icon = guess_title(path.name)
    src = remove_raw_set_page_config(src)
    src = ensure_apply_chrome(src, title, icon)
    if src != orig:
        backup = path.with_suffix(path.suffix + ".bak")
        backup.write_text(orig, encoding="utf-8")
        path.write_text(src, encoding="utf-8")
        return True
    return False

def main():
    repo = Path(".")
    changed = []
    candidates = []
    for p in repo.glob("*.py"):
        if p.name.startswith(("_", "ui_chrome")):
            continue
        candidates.append(p)
    pages_dir = repo / "pages"
    if pages_dir.exists():
        candidates.extend(sorted(pages_dir.glob("*.py")))
    if not candidates:
        print("No candidate .py files found. Run from repo root.")
        sys.exit(1)
    for f in candidates:
        try:
            if patch_file(f):
                changed.append(str(f))
        except Exception as e:
            print(f"!! Failed to patch {f}: {e}")
    print("\nPatched files:")
    for c in changed:
        print("  -", c)
    if not changed:
        print("  (none; already clean)")
    print("\nBackups (*.bak) were created next to originals.")

if __name__ == "__main__":
    main()
