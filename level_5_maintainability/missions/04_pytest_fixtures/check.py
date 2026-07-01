"""Check: Mission 04 — pytest fixtures."""

import json
import subprocess
import sys
from pathlib import Path

mission = Path(__file__).parent
conftest = mission / "conftest.py"
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


# ── conftest.py has fixtures ──────────────────────────────────────────────────

if not conftest.exists():
    print("❌ conftest.py not found")
    raise SystemExit(1)
conf_src = conftest.read_text()
fixture_count = sum(
    1 for ln in conf_src.splitlines()
    if "@pytest.fixture" in ln and not ln.lstrip().startswith("#")
)
if fixture_count < 3:
    print(f"❌ Only {fixture_count} @pytest.fixture found in conftest.py (need ≥ 3)")
    raise SystemExit(1)
for fname in ("warrior", "goblin", "make_hero"):
    if f"def {fname}" not in conf_src:
        print(f"❌ Fixture '{fname}' not found in conftest.py")
        raise SystemExit(1)
print(f"✓ conftest.py has {fixture_count} fixtures (warrior, goblin, make_hero)")

# ── test_combat.py has tests ──────────────────────────────────────────────────

if not test_file.exists():
    print("❌ test_combat.py not found")
    raise SystemExit(1)
test_src = test_file.read_text()
test_count = test_src.count("def test_")
if test_count < 5:
    print(f"❌ Only {test_count} test_ functions found in test_combat.py (need ≥ 5)")
    raise SystemExit(1)
print(f"✓ test_combat.py has {test_count} test functions")

# ── pytest passes ─────────────────────────────────────────────────────────────

result = subprocess.run(
    [sys.executable, "-m", "pytest", str(mission), "-v", "--tb=short", "-q"],
    capture_output=True, text=True, cwd=str(mission),
)
if result.returncode != 0:
    print("❌ pytest fails:")
    print(result.stdout[-3000:])
    raise SystemExit(1)
print("✓ All tests pass")

update_progress("04_pytest_fixtures")
print("\n✅ Mission 04 complete!")
