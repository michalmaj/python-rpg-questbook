"""Check: Mission 01 — ruff linting."""

import json
import subprocess
import sys
from pathlib import Path

task = Path(__file__).parent / "task.py"
pyproject = Path(__file__).parent / "pyproject.toml"
PROGRESS_FILE = Path(__file__).parents[2] / ".progress"


def update_progress(mission_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["missions"][mission_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


# ── pyproject.toml has [tool.ruff.lint] with rules ───────────────────────────

if not pyproject.exists():
    print("❌ pyproject.toml not found in this mission folder")
    raise SystemExit(1)
pycontent = pyproject.read_text()
if "[tool.ruff.lint]" not in pycontent:
    print("❌ [tool.ruff.lint] section not found in pyproject.toml")
    raise SystemExit(1)
if 'select = []' in pycontent or "select = []\n" in pycontent:
    print("❌ ruff select is still empty — add rule categories (e.g. [\"E\", \"F\", \"I\", \"UP\", \"B\"])")
    raise SystemExit(1)
print("✓ pyproject.toml has [tool.ruff.lint] with rules configured")

# ── ruff check must pass ──────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "ruff", "check", str(task), "--config", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ ruff check fails — fix the errors above:")
    print(result.stdout)
    raise SystemExit(1)
print("✓ ruff check passes")

# ── ruff format --check must pass ────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "ruff", "format", "--check", str(task), "--config", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ ruff format --check fails — run: uv run ruff format task.py")
    raise SystemExit(1)
print("✓ ruff format --check passes")

# ── no bare except ────────────────────────────────────────────────────────────

src = task.read_text()
if "except:" in src:
    print("❌ Bare 'except:' still present — ruff E722 should have caught this")
    raise SystemExit(1)
print("✓ No bare except:")

# ── old typing syntax gone ────────────────────────────────────────────────────

for old_syntax in ("Optional[", "List[", "Dict[", "Tuple[", "from typing import Optional"):
    if old_syntax in src:
        print(f"❌ Old typing syntax '{old_syntax}' found — ruff UP rules should fix this")
        raise SystemExit(1)
print("✓ No deprecated typing syntax (Optional, List, Dict from typing)")

update_progress("01_ruff_linting")
print("\n✅ Mission 01 complete!")
