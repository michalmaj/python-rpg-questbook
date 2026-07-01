"""Check: Mission 05 — pytest parametrize."""

import json
import subprocess
import sys
from pathlib import Path

mission = Path(__file__).parent
test_file = mission / "test_combat.py"
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


# ── @pytest.mark.parametrize used ≥ 2 times ──────────────────────────────────

if not test_file.exists():
    print("❌ test_combat.py not found")
    raise SystemExit(1)
src = test_file.read_text()
param_count = sum(
    1 for ln in src.splitlines()
    if "@pytest.mark.parametrize" in ln and not ln.lstrip().startswith("#")
)
if param_count < 2:
    print(f"❌ Only {param_count} @pytest.mark.parametrize found (need ≥ 2)")
    raise SystemExit(1)
print(f"✓ {param_count} @pytest.mark.parametrize decorators found")

# ── ids= used in at least one parametrize call ───────────────────────────────

if not any(
    "@pytest.mark.parametrize" in ln and "ids=" in ln and not ln.lstrip().startswith("#")
    for ln in src.splitlines()
):
    print("❌ ids= not found — add ids=[...] to at least one @pytest.mark.parametrize call")
    raise SystemExit(1)
print("✓ ids= used in at least one parametrize call")

# ── pytest passes ─────────────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "pytest", str(mission), "-v", "--tb=short"],
    capture_output=True, text=True, cwd=str(mission),
)
if result.returncode != 0:
    print("❌ pytest fails:")
    print(result.stdout[-3000:])
    raise SystemExit(1)

# Count collected test cases (parametrize multiplies them)
collected = [ln for ln in result.stdout.splitlines() if " PASSED" in ln]
if len(collected) < 8:
    print(f"❌ Only {len(collected)} test cases collected (need ≥ 8, parametrize should multiply them)")
    raise SystemExit(1)
print(f"✓ {len(collected)} test cases pass (including parametrized cases)")

update_progress("05_pytest_parametrize")
print("\n✅ Mission 05 complete!")
