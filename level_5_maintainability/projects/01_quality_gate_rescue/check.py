"""check.py — Project 01: Quality Gate Rescue"""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[3] / "level_5_maintainability" / ".progress"


def update_progress(project_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["projects"][project_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def run_tool(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_DIR))


def main() -> None:
    # ── 1. ruff check passes ──────────────────────────────────────────────────
    result = run_tool([sys.executable, "-m", "ruff", "check", "rpg/"])
    if result.returncode != 0:
        print("❌ ruff check rpg/ still has violations:")
        print(result.stdout or result.stderr)
        print()
        print("Fix all ruff violations, then run check.py again.")
        raise SystemExit(1)
    print("✓ ruff check rpg/ — 0 violations")

    # ── 2. mypy --strict passes ───────────────────────────────────────────────
    result = run_tool([sys.executable, "-m", "mypy", "--strict", "rpg/"])
    if result.returncode != 0:
        print("❌ mypy --strict rpg/ still has errors:")
        print(result.stdout or result.stderr)
        print()
        print("Fix all mypy errors (add annotations, remove Any), then run check.py again.")
        raise SystemExit(1)
    print("✓ mypy --strict rpg/ — 0 errors")

    # ── 3. pyright passes ────────────────────────────────────────────────────
    result = run_tool(["pyright", "rpg/"])
    if result.returncode != 0:
        # pyright might not be installed — warn but don't block
        if "not found" in result.stderr.lower() or "no such file" in result.stderr.lower():
            print("⚠  pyright not installed — skipping (install with: uv add --dev pyright)")
        else:
            print("❌ pyright rpg/ still has errors:")
            print(result.stdout or result.stderr)
            print()
            print("Fix all pyright errors, then run check.py again.")
            raise SystemExit(1)
    else:
        print("✓ pyright rpg/ — 0 errors")

    # ── 4. QUALITY_REPORT.md exists ───────────────────────────────────────────
    report = PROJECT_DIR / "QUALITY_REPORT.md"
    if not report.exists():
        print("❌ QUALITY_REPORT.md not found")
        print("   Create it and describe what each tool found (≥3 sections).")
        raise SystemExit(1)
    print("✓ QUALITY_REPORT.md exists")

    # ── 5. Report has ≥3 sections ─────────────────────────────────────────────
    content = report.read_text(encoding="utf-8")
    sections = [ln for ln in content.splitlines() if ln.startswith("## ")]
    if len(sections) < 3:
        print(f"❌ QUALITY_REPORT.md must have ≥3 sections (## headers), found {len(sections)}")
        raise SystemExit(1)
    print(f"✓ QUALITY_REPORT.md has {len(sections)} sections")

    # ── 6. Report mentions all three tools ────────────────────────────────────
    lower = content.lower()
    for tool in ("ruff", "mypy", "pyright"):
        if tool not in lower:
            print(f"❌ QUALITY_REPORT.md must mention '{tool}'")
            raise SystemExit(1)
    print("✓ QUALITY_REPORT.md mentions ruff, mypy, and pyright")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("01_quality_gate_rescue")
    print()
    print("✅ Project 01 complete: Quality Gate Rescue!")
    print()
    print("   ruff + mypy + pyright all pass. The codebase is clean.")
    print("   You know what each tool finds — and that they find different things.")


if __name__ == "__main__":
    main()
