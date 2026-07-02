"""Check: Mission 02 — mypy type checking."""

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


# ── pyproject.toml has [tool.mypy] ───────────────────────────────────────────

if not pyproject.exists():
    print("❌ pyproject.toml not found in this mission folder")
    raise SystemExit(1)
if "[tool.mypy]" not in pyproject.read_text():
    print("❌ [tool.mypy] section not found in pyproject.toml")
    raise SystemExit(1)
print("✓ pyproject.toml has [tool.mypy]")

# ── ruff must still pass ──────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "ruff", "check", str(task), "--config", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ ruff check fails (regression — task.py should stay ruff-clean):")
    print(result.stdout)
    raise SystemExit(1)
print("✓ ruff check still passes")

# ── mypy --strict must pass ───────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "mypy", str(task), "--strict",
     "--config-file", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ mypy --strict fails:")
    print(result.stdout)
    raise SystemExit(1)
print("✓ mypy --strict passes")

# ── at least 8 annotated function signatures ──────────────────────────────────

src = task.read_text()
annotated = [ln for ln in src.splitlines() if "def " in ln and " -> " in ln]
if len(annotated) < 8:
    print(f"❌ Only {len(annotated)} annotated function signatures (need ≥ 8)")
    print("   Make sure all top-level functions and class methods have return types")
    raise SystemExit(1)
print(f"✓ {len(annotated)} annotated function signatures")

# ── no bare except ────────────────────────────────────────────────────────────

if "except:" in src:
    print("❌ Bare 'except:' still present — use 'except Exception as e:'")
    raise SystemExit(1)
print("✓ No bare except:")

# ── no old typing syntax ──────────────────────────────────────────────────────

for old in ("Optional[", "List[", "Dict[", "from typing import Optional"):
    if old in src:
        print(f"❌ Old typing syntax '{old}' found — use X | None, list[...], dict[...]")
        raise SystemExit(1)
print("✓ No deprecated typing syntax")

update_progress("02_mypy_type_checking")
print("\n✅ Mission 02 complete!")
