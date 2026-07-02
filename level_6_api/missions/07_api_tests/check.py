# level_6_api/missions/07_api_tests/check.py
"""Check: Mission 07 — API Tests."""
import json
import os
import subprocess
import sys
from pathlib import Path

PROGRESS_FILE = Path(__file__).parents[2] / ".progress"
mission = Path(__file__).parent


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


# ── test file exists ──────────────────────────────────────────────────────────

test_file = mission / "task/tests/test_api.py"
if not test_file.exists():
    print("❌ task/tests/test_api.py not found — create your test file")
    raise SystemExit(1)

src = test_file.read_text()

# ── TestClient used ───────────────────────────────────────────────────────────

if "TestClient" not in src:
    print("❌ TestClient not used in test_api.py")
    raise SystemExit(1)
print("✓ TestClient used in test_api.py")

# ── dependency_overrides used (session isolation) ─────────────────────────────

if "dependency_overrides" not in src:
    print("❌ app.dependency_overrides not used — isolate SessionRepository in tests with tmp_path")
    raise SystemExit(1)
print("✓ dependency_overrides used for test isolation")

# ── no unittest.mock or @patch ────────────────────────────────────────────────

code_lines = [ln for ln in src.splitlines() if not ln.lstrip().startswith("#")]
code_src = "\n".join(code_lines)
if "unittest.mock" in code_src or "@patch" in code_src:
    print("❌ unittest.mock / @patch found — use app.dependency_overrides instead")
    raise SystemExit(1)
print("✓ No unittest.mock or @patch — clean dependency_overrides approach")

# ── at least 6 test functions ─────────────────────────────────────────────────

test_fn_count = sum(
    1 for ln in src.splitlines()
    if ln.lstrip().startswith("def test_") and not ln.lstrip().startswith("#")
)
if test_fn_count < 6:
    print(f"❌ Found {test_fn_count} test functions — write at least 6")
    raise SystemExit(1)
print(f"✓ {test_fn_count} test functions found")

# ── pytest passes ─────────────────────────────────────────────────────────────

env = os.environ.copy()
env["PYTHONPATH"] = str(mission)
result = subprocess.run(
    [sys.executable, "-m", "pytest", "task/tests/test_api.py", "-q", "--tb=short"],
    capture_output=True, text=True, cwd=str(mission), env=env,
)
if result.returncode != 0:
    print("❌ pytest fails:")
    print(result.stdout[-2000:])
    print(result.stderr[-500:])
    raise SystemExit(1)
print("✓ All API tests pass")

update_progress("07_api_tests")
print("\n✅ Mission 07 complete!")
