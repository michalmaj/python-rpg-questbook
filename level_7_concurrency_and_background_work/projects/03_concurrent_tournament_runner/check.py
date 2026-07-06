"""Check: Boss Fight — Concurrent Tournament Runner."""
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

project = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[2] / ".progress"
sys.path.insert(0, str(project))


def update_progress(project_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["projects"][project_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


print("Checking boss fight: concurrent_tournament_runner")
print("=" * 50)

# ── Gate 1: import app ────────────────────────────────────────────────────────
try:
    from api.main import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import app from api.main: {exc}")
    raise SystemExit(1)

import warnings
warnings.filterwarnings("ignore")
from fastapi.testclient import TestClient
from api.dependencies import get_job_repo, get_worker
from jobs.jobs import InMemoryJobRepository, SyncWorker

_repo = InMemoryJobRepository()
_worker = SyncWorker(_repo)
app.dependency_overrides[get_job_repo] = lambda: _repo
app.dependency_overrides[get_worker] = lambda: _worker
client = TestClient(app, raise_server_exceptions=False)

# ── Gate 2: GET /health ───────────────────────────────────────────────────────
r = client.get("/health")
if r.status_code != 200:
    print(f"❌ GET /health returned {r.status_code}")
    raise SystemExit(1)
print("✓ GET /health → 200")

# ── Gate 3: POST /tournaments → 202 + job_id ─────────────────────────────────
r = client.post("/tournaments", json={"battles": 20})
if r.status_code != 202:
    print(f"❌ POST /tournaments should return 202, got {r.status_code}: {r.text[:200]}")
    raise SystemExit(1)
job_id = r.json().get("job_id")
if not job_id:
    print("❌ POST /tournaments missing job_id")
    raise SystemExit(1)
print(f"✓ POST /tournaments → 202, job_id={job_id[:8]}...")

# ── Gate 4: GET /tournaments/{job_id} → completed (SyncWorker) ───────────────
r = client.get(f"/tournaments/{job_id}")
if r.status_code != 200:
    print(f"❌ GET /tournaments/{job_id} → {r.status_code}")
    raise SystemExit(1)
data = r.json()
if data.get("status") != "completed":
    print(f"❌ Job status should be 'completed' (SyncWorker), got {data.get('status')}")
    raise SystemExit(1)
if not data.get("result"):
    print("❌ Job result is empty")
    raise SystemExit(1)
print(f"✓ GET /tournaments/{job_id[:8]}... → completed, result={data['result']}")

# ── Gate 5: GET /tournaments/{job_id}/report → Markdown ─────────────────────
r = client.get(f"/tournaments/{job_id}/report")
if r.status_code != 200:
    print(f"❌ GET /tournaments/{job_id}/report → {r.status_code}")
    raise SystemExit(1)
if "text/plain" not in r.headers.get("content-type", ""):
    print(f"❌ Report content-type is not text/plain: {r.headers.get('content-type')}")
    raise SystemExit(1)
if "## Tournament Report" not in r.text:
    print("❌ Report missing '## Tournament Report' header")
    raise SystemExit(1)
print("✓ GET /tournaments/{id}/report → Markdown with ## Tournament Report")

# ── Gate 6: unknown job → 404 ────────────────────────────────────────────────
r = client.get("/tournaments/nonexistent-xyz")
if r.status_code != 404:
    print(f"❌ Unknown job should be 404, got {r.status_code}")
    raise SystemExit(1)
print("✓ GET /tournaments/nonexistent → 404")

# ── Gate 7: invalid battles → 422 ────────────────────────────────────────────
r = client.post("/tournaments", json={"battles": 0})
if r.status_code != 422:
    print(f"❌ battles=0 should be 422, got {r.status_code}")
    raise SystemExit(1)
print("✓ POST /tournaments battles=0 → 422")

# ── Gate 8: report for incomplete job → 425 ──────────────────────────────────
from jobs.jobs import InMemoryJobRepository as IMJR, BackgroundWorker
_repo2 = IMJR()
_slow_started = threading.Event()
_slow_done = threading.Event()


def _slow_fn() -> dict:
    _slow_started.set()
    _slow_done.wait(timeout=5)
    return {"total_battles": 1, "hero_wins": 1, "monster_wins": 0, "hero_win_rate": 1.0}


_bw = BackgroundWorker(_repo2)
app.dependency_overrides[get_job_repo] = lambda: _repo2
app.dependency_overrides[get_worker] = lambda: _bw

_repo2.create("slow-job")
_bw.submit("slow-job", _slow_fn)
_slow_started.wait(timeout=2)
r2 = client.get("/tournaments/slow-job/report")
_slow_done.set()
if r2.status_code != 425:
    print(f"❌ Report for running job should be 425, got {r2.status_code}")
    raise SystemExit(1)
print("✓ GET report for running job → 425")

# restore SyncWorker for pytest gate
app.dependency_overrides[get_job_repo] = lambda: _repo
app.dependency_overrides[get_worker] = lambda: _worker

# ── Gate 9: at least 6 test functions ────────────────────────────────────────
import ast as _ast

_test_file = project / "tests" / "test_api.py"
_test_src = _test_file.read_text()
_test_tree = _ast.parse(_test_src)
_test_funcs = [
    n.name for n in _ast.walk(_test_tree)
    if isinstance(n, _ast.FunctionDef) and n.name.startswith("test_")
]
if len(_test_funcs) < 6:
    print(f"❌ tests/test_api.py has {len(_test_funcs)} test function(s); at least 6 required")
    raise SystemExit(1)
print(f"✓ tests/test_api.py has {len(_test_funcs)} test functions (≥6 required)")

# ── Gate 10: pytest test_api.py ───────────────────────────────────────────────
app.dependency_overrides.clear()
env = os.environ.copy()
env["PYTHONPATH"] = str(project)
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_api.py", "-q", "--tb=short"],
    capture_output=True, text=True, cwd=str(project), env=env,
)
if result.returncode != 0:
    print("❌ pytest tests/test_api.py fails:")
    print(result.stdout[-2000:])
    raise SystemExit(1)
print(f"✓ All {len(_test_funcs)} API tests pass")

# ── Gate 11: ProcessPoolExecutor inside ProcessPoolTournamentWorker ────────────
import ast as _ast

_jobs_src = (project / "jobs" / "jobs.py").read_text(encoding="utf-8")
_jobs_tree = _ast.parse(_jobs_src)

_found_pptw = False
_uses_ppe_inside = False
for _node in _ast.walk(_jobs_tree):
    if isinstance(_node, _ast.ClassDef) and _node.name == "ProcessPoolTournamentWorker":
        _found_pptw = True
        for _child in _ast.walk(_node):
            if isinstance(_child, _ast.Name) and _child.id == "ProcessPoolExecutor":
                _uses_ppe_inside = True
            if isinstance(_child, _ast.Attribute) and _child.attr == "ProcessPoolExecutor":
                _uses_ppe_inside = True

if not _found_pptw:
    print("❌ ProcessPoolTournamentWorker class not found in jobs/jobs.py")
    raise SystemExit(1)
if not _uses_ppe_inside:
    print("❌ ProcessPoolTournamentWorker must use ProcessPoolExecutor internally")
    raise SystemExit(1)
print("✓ ProcessPoolTournamentWorker uses ProcessPoolExecutor for parallel battles")

update_progress("03_concurrent_tournament_runner")
print()
print("✅ Boss fight complete! Concurrent Tournament Runner operational.")
print("   POST /tournaments ✓  job tracking ✓  Markdown reports ✓  tests ✓")
print("   ProcessPoolExecutor ✓  CPU-bound battles run in parallel across cores")
