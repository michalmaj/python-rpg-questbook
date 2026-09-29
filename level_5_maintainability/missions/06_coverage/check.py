"""Check: Mission 06 — coverage.

The starter test suite (inherited from M04/M05) already covers 98% of
rpg.py (97% branch coverage) before the student does anything — the only
gap is simulate_turn's "both survive" outcome. A threshold of 80% would
let the mission pass on config alone, with no new test required. This
checker requires branch coverage at 100% instead (the exact, measured
size of the real gap — not an arbitrary round number), and additionally
runs a single targeted mutant on that exact gap so that a test which
merely *executes* the missing branch without asserting anything on its
result (inflating coverage without checking behavior) still fails.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

mission = Path(__file__).parent
pyproject = mission / "pyproject.toml"
rpg_file = mission / "rpg.py"
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


def _clear_caches() -> None:
    shutil.rmtree(mission / "__pycache__", ignore_errors=True)
    shutil.rmtree(mission / ".pytest_cache", ignore_errors=True)
    (mission / ".coverage").unlink(missing_ok=True)


# ── pyproject.toml has [tool.coverage] with branch = true ────────────────────

if not pyproject.exists():
    print("❌ pyproject.toml not found")
    raise SystemExit(1)
pyproject_src = pyproject.read_text()
if "[tool.coverage" not in pyproject_src:
    print("❌ [tool.coverage] section not found in pyproject.toml")
    print("   Add [tool.coverage.run] and [tool.coverage.report] sections")
    raise SystemExit(1)
run_section = pyproject_src.split("[tool.coverage.run]")[-1].split("[tool.coverage.report]")[0] \
    if "[tool.coverage.run]" in pyproject_src else ""
if "branch" not in run_section or "true" not in run_section.lower():
    print("❌ [tool.coverage.run] must set branch = true")
    print("   Line coverage alone can miss an untested branch inside a line "
          "that IS otherwise executed — branch coverage checks that both "
          "outcomes of a decision were exercised.")
    raise SystemExit(1)
print("✓ pyproject.toml has [tool.coverage] with branch = true")

# ── pytest passes ─────────────────────────────────────────────────────────────

_clear_caches()
result = subprocess.run(
    [sys.executable, "-m", "pytest", str(mission), "-q", "--tb=short"],
    capture_output=True, text=True, cwd=str(mission),
)
_clear_caches()
if result.returncode != 0:
    print("❌ pytest fails:")
    print(result.stdout[-2000:])
    raise SystemExit(1)
print("✓ All tests pass")

# ── branch coverage == 100% for rpg.py ────────────────────────────────────────
#
# The gap here is small and precisely known (one branch), so 100% is not an
# arbitrary target — it's exactly "close the one real gap the baseline
# leaves open". --cov-branch is passed explicitly on the command line rather
# than trusted from pyproject.toml alone, since this repo's pytest-cov/
# coverage versions do not reliably auto-apply [tool.coverage.run] settings
# without it.

_clear_caches()
cov_result = subprocess.run(
    [sys.executable, "-m", "pytest", str(mission),
     "--cov=rpg", "--cov-branch", "--cov-report=term-missing", "-q"],
    capture_output=True, text=True, cwd=str(mission),
)
_clear_caches()
output = cov_result.stdout + cov_result.stderr
match = re.search(r"rpg\.py[^\n]*?(\d+)%", output)
if not match:
    print("❌ Could not find branch coverage for rpg.py in output")
    print("   Make sure pytest-cov is installed: uv add --dev pytest-cov")
    print(output[-2000:])
    raise SystemExit(1)
pct = int(match.group(1))
if pct < 100:
    print(f"❌ Branch coverage for rpg.py is {pct}% (need 100%)")
    print("   Look at the 'Missing' column above — one behavior is never "
          "exercised by any test. Add a test for it.")
    raise SystemExit(1)
print(f"✓ Branch coverage for rpg.py: {pct}%")

# ── the specific gap must be behaviorally tested, not just executed ──────────
#
# 100% coverage only proves every line and branch RAN during the suite — not
# that anything meaningful was asserted about the result. A test that calls
# simulate_turn() on a "both survive" case with no assertion on the outcome
# would already satisfy the coverage number above. This mutant flips that
# exact outcome and requires some test to actually notice.

if not rpg_file.exists():
    print("❌ rpg.py not found")
    raise SystemExit(1)
original_rpg_src = rpg_file.read_text()

MUTANT_LABEL = "simulate_turn: the 'both survive' outcome is reported backwards"
OLD = "        return False, True\n    return True, True"
NEW = "        return False, True\n    return False, False"

if OLD not in original_rpg_src:
    print(f"❌ internal check error: mutant anchor not found for: {MUTANT_LABEL}")
    raise SystemExit(1)

try:
    rpg_file.write_text(original_rpg_src.replace(OLD, NEW, 1))
    _clear_caches()
    mutant_result = subprocess.run(
        [sys.executable, "-m", "pytest", str(mission), "-q", "--tb=line"],
        capture_output=True, text=True, cwd=str(mission),
    )
    _clear_caches()
finally:
    rpg_file.write_text(original_rpg_src)
    _clear_caches()

if rpg_file.read_text() != original_rpg_src:
    print("❌ internal check error: rpg.py was not restored correctly — please re-run")
    raise SystemExit(1)

if mutant_result.returncode == 0:
    print(f"❌ Your tests reached 100% coverage but didn't catch this bug: {MUTANT_LABEL}.")
    print("   Reaching a line/branch isn't the same as checking what it returns — "
          "add an assertion on the actual hero_alive/monster_alive values for the "
          "'both survive' case, not just a call that executes it.")
    raise SystemExit(1)
print(f"✓ tests correctly fail when: {MUTANT_LABEL}")

update_progress("06_coverage")
print("\n✅ Mission 06 complete!")
