"""Check: Mission 09 — GitHub Actions CI."""

import json
import subprocess
import sys
from pathlib import Path

mission = Path(__file__).parent
ci_yml = mission / ".github" / "workflows" / "ci.yml"
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


# ── .github/workflows/ci.yml exists ──────────────────────────────────────────

if not ci_yml.exists():
    print("❌ .github/workflows/ci.yml not found in this mission folder")
    print("   Create the directory structure and file:")
    print("   mkdir -p .github/workflows")
    print("   touch .github/workflows/ci.yml")
    raise SystemExit(1)
content = ci_yml.read_text()
print("✓ .github/workflows/ci.yml found")

# ── required CI elements ──────────────────────────────────────────────────────

required = {
    "on:": "trigger (on:)",
    "jobs:": "jobs: section",
    "uv": "uv setup step",
    "ruff": "ruff check step",
    "mypy": "mypy step",
    "pytest": "pytest step",
    "3.12": "Python 3.12 in matrix",
    "3.13": "Python 3.13 in matrix",
}
for keyword, label in required.items():
    if keyword not in content:
        print(f"❌ {label} ({keyword!r}) not found in ci.yml")
        raise SystemExit(1)
print("✓ ci.yml has trigger, jobs, uv, ruff, mypy, pytest, matrix [3.12, 3.13]")

# ── steps are in correct order: ruff before mypy before pytest ───────────────

# Check step ordering: ruff → mypy → pytest
run_lines = [(i, ln) for i, ln in enumerate(content.splitlines()) if "run:" in ln]
ruff_lines = [i for i, ln in run_lines if "ruff" in ln]
mypy_lines = [i for i, ln in run_lines if "mypy" in ln]
pytest_lines = [i for i, ln in run_lines if "pytest" in ln]
if not ruff_lines or not mypy_lines or not pytest_lines:
    print("❌ ci.yml must have run: steps for ruff, mypy, and pytest")
    raise SystemExit(1)
if not (min(ruff_lines) < min(mypy_lines) < min(pytest_lines)):
    print("❌ Step order must be: ruff → mypy → pytest")
    print("   (ruff catches style issues before type checking)")
    raise SystemExit(1)
print("✓ Step ordering correct: ruff → mypy → pytest")

# ── local tools pass on task.py ──────────────────────────────────────────────

task_py = mission / "task.py"

result = subprocess.run(
    [sys.executable, "-m", "ruff", "check", str(task_py)],
    capture_output=True,
    text=True,
)
if result.returncode != 0:
    print("❌ ruff check failed on task.py:")
    print(result.stdout or result.stderr)
    raise SystemExit(1)
print("✓ ruff check passes on task.py")

result = subprocess.run(
    [sys.executable, "-m", "mypy", str(task_py), "--strict"],
    capture_output=True,
    text=True,
)
if result.returncode != 0:
    print("❌ mypy --strict failed on task.py:")
    print(result.stdout or result.stderr)
    raise SystemExit(1)
print("✓ mypy --strict passes on task.py")

update_progress("09_github_actions_ci")
print("\n✅ Mission 09 complete!")
print("   To see this CI run for real: copy .github/workflows/ci.yml to your repo root and push.")
