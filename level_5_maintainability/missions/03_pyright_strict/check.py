"""Check: Mission 03 — pyright strict."""

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


# ── pyproject.toml has [tool.pyright] ────────────────────────────────────────

if not pyproject.exists():
    print("❌ pyproject.toml not found in this mission folder")
    raise SystemExit(1)
pycontent = pyproject.read_text()
if "[tool.pyright]" not in pycontent:
    print("❌ [tool.pyright] section not found in pyproject.toml")
    raise SystemExit(1)
if "strict" not in pycontent.split("[tool.pyright]")[1].split("[")[0]:
    print("❌ [tool.pyright] section must include typeCheckingMode = \"strict\"")
    raise SystemExit(1)
print("✓ pyproject.toml has [tool.pyright] with strict mode")

# ── mypy --strict must still pass (regression check) ─────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "mypy", str(task), "--strict",
     "--config-file", str(pyproject)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ mypy --strict regression — task.py broke since M02:")
    print(result.stdout)
    raise SystemExit(1)
print("✓ mypy --strict still passes")

# ── pyright must pass ─────────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "pyright", str(task), "--project", str(pyproject.parent)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    print("❌ pyright fails:")
    print(result.stdout[-3000:])
    raise SystemExit(1)
print("✓ pyright passes")

update_progress("03_pyright_strict")
print("\n✅ Mission 03 complete!")
