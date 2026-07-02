"""Check: Mission 06 — coverage."""

import json
import re
import subprocess
import sys
from pathlib import Path

mission = Path(__file__).parent
pyproject = mission / "pyproject.toml"
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


# ── pyproject.toml has [tool.coverage] ───────────────────────────────────────

if not pyproject.exists():
    print("❌ pyproject.toml not found")
    raise SystemExit(1)
if "[tool.coverage" not in pyproject.read_text():
    print("❌ [tool.coverage] section not found in pyproject.toml")
    print("   Add [tool.coverage.run] and [tool.coverage.report] sections")
    raise SystemExit(1)
print("✓ pyproject.toml has [tool.coverage] config")

# ── pytest passes ─────────────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "pytest", str(mission), "-q", "--tb=short"],
    capture_output=True, text=True, cwd=str(mission),
)
if result.returncode != 0:
    print("❌ pytest fails:")
    print(result.stdout[-2000:])
    raise SystemExit(1)
print("✓ All tests pass")

# ── coverage ≥ 80% for rpg.py ────────────────────────────────────────────────

cov_result = subprocess.run(
    [sys.executable, "-m", "pytest", str(mission),
     "--cov=rpg", "--cov-report=term-missing", "-q"],
    capture_output=True, text=True, cwd=str(mission),
)
output = cov_result.stdout + cov_result.stderr
match = re.search(r"rpg\.py\s+\d+\s+\d+\s+(\d+)%", output)
if not match:
    print("❌ Could not find coverage for rpg.py in output")
    print("   Make sure pytest-cov is installed: uv add --dev pytest-cov")
    print(output[-2000:])
    raise SystemExit(1)
pct = int(match.group(1))
if pct < 80:
    print(f"❌ Coverage for rpg.py is {pct}% (need ≥ 80%)")
    print("   Add tests for uncovered branches (check the 'Missing' column)")
    raise SystemExit(1)
print(f"✓ Coverage for rpg.py: {pct}%")

update_progress("06_coverage")
print("\n✅ Mission 06 complete!")
