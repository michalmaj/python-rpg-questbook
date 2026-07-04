"""Check: Mission 08 — Testing Background Work."""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
mission = Path(__file__).parent
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


test_file = mission / "task" / "tests" / "test_background.py"
if not test_file.exists():
    print("❌ task/tests/test_background.py not found")
    raise SystemExit(1)

src = test_file.read_text()

# SyncWorker used
if "SyncWorker" not in src:
    print("❌ SyncWorker not imported/used in test_background.py")
    raise SystemExit(1)
print("✓ SyncWorker used in tests")

# no time.sleep
code_lines = [ln for ln in src.splitlines() if not ln.lstrip().startswith("#")]
if "time.sleep" in "\n".join(code_lines):
    print("❌ time.sleep() found — use SyncWorker for deterministic tests")
    raise SystemExit(1)
print("✓ No time.sleep() — deterministic tests")

# at least 6 test functions
test_fn_count = sum(1 for ln in src.splitlines()
                    if ln.lstrip().startswith("def test_") and not ln.lstrip().startswith("#"))
if test_fn_count < 6:
    print(f"❌ Found {test_fn_count} test functions — write at least 6")
    raise SystemExit(1)
print(f"✓ {test_fn_count} test functions found")

# pytest passes
env = os.environ.copy()
env["PYTHONPATH"] = str(mission)
result = subprocess.run(
    [sys.executable, "-m", "pytest", "task/tests/test_background.py", "-q", "--tb=short"],
    capture_output=True, text=True, cwd=str(mission), env=env,
)
if result.returncode != 0:
    print("❌ pytest fails:")
    print(result.stdout[-2000:])
    print(result.stderr[-500:])
    raise SystemExit(1)
print("✓ All background tests pass")

update_progress("08_testing_background_work")
print("\n✅ Mission 08 complete! Deterministic tests for background work.")
