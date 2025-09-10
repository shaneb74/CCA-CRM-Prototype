
# patch_store_autohide.py — inject auto-hide into your existing store.py (non-destructive)
"""
Usage:
  python patch_store_autohide.py /path/to/your/repo

What it does:
  - Opens <repo>/store.py
  - If it doesn't already import/call hide_default(), injects this near the top:
        try:
            from ui_chrome import hide_default
            hide_default()
        except Exception:
            pass
  - Writes a backup store.py.bak alongside the original.
"""
import sys, pathlib, re

SNIPPET = """try:
    from ui_chrome import hide_default
    hide_default()
except Exception:
    pass

"""

def already_patched(code: str) -> bool:
    return "hide_default()" in code and "ui_chrome" in code

def inject(code: str) -> str:
    # Insert after the initial import block (after first blank line following imports)
    # Fallbacks: after first "import streamlit as st", else at very top.
    m = re.search(r"^(import .+?\n(?:from .+?\n|import .+?\n)*\n)", code, flags=re.MULTILINE)
    if m:
        pos = m.end()
        return code[:pos] + SNIPPET + code[pos:]
    m2 = re.search(r"(import\s+streamlit\s+as\s+st\s*\n)", code)
    if m2:
        pos = m2.end()
        return code[:pos] + SNIPPET + code[pos:]
    return SNIPPET + code

def main():
    if len(sys.argv) != 2:
        print("Usage: python patch_store_autohide.py /path/to/your/repo")
        sys.exit(1)
    repo = pathlib.Path(sys.argv[1]).expanduser().resolve()
    target = repo / "store.py"
    if not target.exists():
        print(f"Error: {target} not found")
        sys.exit(2)
    code = target.read_text(encoding="utf-8")
    if already_patched(code):
        print("store.py already contains hide_default(); no changes made.")
        return
    (repo / "store.py.bak").write_text(code, encoding="utf-8")
    target.write_text(inject(code), encoding="utf-8")
    print("Patched store.py. Backup written to store.py.bak")
if __name__ == "__main__":
    main()
