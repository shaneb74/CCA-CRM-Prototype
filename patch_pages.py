
# patch_pages.py — non-destructive injector for hide_default()
"""
Usage:
  python patch_pages.py /path/to/your/repo

What it does:
  - Finds these files in <repo>/pages/: 
      01_Dashboard.py, 02_Advisor_Workspace.py, 03_Notifications.py, 
      04_Client_Record.py, 05_Supervisor_Workspace.py
  - Inserts two lines immediately AFTER the first st.set_page_config(...):
        from ui_chrome import hide_default
        hide_default()
  - Skips any file that already imports/calls hide_default().
  - Writes a .bak backup next to each edited file.
"""
import sys, re, pathlib

VISIBLE = [
    "01_Dashboard.py",
    "02_Advisor_Workspace.py",
    "03_Notifications.py",
    "04_Client_Record.py",
    "05_Supervisor_Workspace.py",
]

INJECT = "from ui_chrome import hide_default\nhide_default()\n"

def already_has(code: str) -> bool:
    return "hide_default()" in code

def inject_after_set_page_config(code: str) -> str:
    # Find the first occurrence of st.set_page_config(...)\n
    pat = re.compile(r"(st\.set_page_config\([^\n]*\)\s*\n)", re.MULTILINE)
    m = pat.search(code)
    if not m:
        # No set_page_config; inject at top after first import streamlit as st
        pat2 = re.compile(r"(import\s+streamlit\s+as\s+st\s*\n)", re.MULTILINE)
        m2 = pat2.search(code)
        if m2:
            insert_at = m2.end()
            return code[:insert_at] + INJECT + code[insert_at:]
        # Fallback: put at very top
        return INJECT + code
    insert_at = m.end()
    return code[:insert_at] + INJECT + code[insert_at:]

def main():
    if len(sys.argv) != 2:
        print("Usage: python patch_pages.py /path/to/your/repo")
        sys.exit(1)
    repo = pathlib.Path(sys.argv[1]).expanduser().resolve()
    pages = repo / "pages"
    if not pages.exists():
        print(f"Error: {pages} not found")
        sys.exit(2)
    edited = 0
    for fname in VISIBLE:
        fpath = pages / fname
        if not fpath.exists():
            print(f"Skip (missing): {fname}")
            continue
        code = fpath.read_text(encoding="utf-8")
        if already_has(code):
            print(f"Skip (already patched): {fname}")
            continue
        new_code = inject_after_set_page_config(code)
        # backup
        (pages / (fname + ".bak")).write_text(code, encoding="utf-8")
        fpath.write_text(new_code, encoding="utf-8")
        print(f"Patched: {fname}")
        edited += 1
    if edited == 0:
        print("No files changed.")
    else:
        print(f"Done. Patched {edited} file(s).")
if __name__ == "__main__":
    main()
