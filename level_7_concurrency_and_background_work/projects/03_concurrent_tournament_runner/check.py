"""Check: Boss Fight — Concurrent Tournament Runner.

ProcessPoolExecutor (macOS "spawn" start method) re-imports this script in each
worker process. Without the `if __name__ == '__main__':` guard below, every spawned
worker would re-run all the check logic, causing recursive spawning and BrokenProcessPool
errors. Keep all executable logic inside the guard.
"""
import ast as _ast
import inspect
import json
import os
import pickle
import subprocess
import sys
import time
from pathlib import Path

project = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[2] / ".progress"
sys.path.insert(0, str(project))

# Minimal module-level import so worker processes can resolve project modules.
# DO NOT add check logic here — it would run in worker processes too.
try:
    from api.main import app  # type: ignore[import]
except ImportError:
    app = None  # caught inside the guard

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")

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

    # ── Gate 1: import app ────────────────────────────────────────────────────
    if app is None:
        print("❌ Cannot import app from api.main")
        raise SystemExit(1)

    from fastapi.testclient import TestClient
    from api.dependencies import get_job_repo, get_worker
    from jobs.jobs import InMemoryJobRepository, SyncWorker, JobStatus

    _repo = InMemoryJobRepository()
    _worker = SyncWorker(_repo)
    app.dependency_overrides[get_job_repo] = lambda: _repo
    app.dependency_overrides[get_worker] = lambda: _worker
    client = TestClient(app, raise_server_exceptions=False)

    # ── Gate 2: GET /health ───────────────────────────────────────────────────
    r = client.get("/health")
    if r.status_code != 200:
        print(f"❌ GET /health returned {r.status_code}")
        raise SystemExit(1)
    print("✓ GET /health → 200")

    # ── Gate 3: POST /tournaments → 202 + job_id ─────────────────────────────
    r = client.post("/tournaments", json={"battles": 20})
    if r.status_code != 202:
        print(f"❌ POST /tournaments should return 202, got {r.status_code}: {r.text[:200]}")
        raise SystemExit(1)
    job_id = r.json().get("job_id")
    if not job_id:
        print("❌ POST /tournaments missing job_id")
        raise SystemExit(1)
    print(f"✓ POST /tournaments → 202, job_id={job_id[:8]}...")

    # ── Gate 4: GET /tournaments/{job_id} → completed (SyncWorker) ───────────
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

    # ── Gate 5: GET /tournaments/{job_id}/report → Markdown ──────────────────
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

    # ── Gate 6: unknown job → 404 ─────────────────────────────────────────────
    r = client.get("/tournaments/nonexistent-xyz")
    if r.status_code != 404:
        print(f"❌ Unknown job should be 404, got {r.status_code}")
        raise SystemExit(1)
    print("✓ GET /tournaments/nonexistent → 404")

    # ── Gate 7: invalid battles → 422 ────────────────────────────────────────
    r = client.post("/tournaments", json={"battles": 0})
    if r.status_code != 422:
        print(f"❌ battles=0 should be 422, got {r.status_code}")
        raise SystemExit(1)
    print("✓ POST /tournaments battles=0 → 422")

    # ── Gate 8: report for incomplete job → 425 ──────────────────────────────
    # Manually set a job to "running" — no threading or sleep needed.
    _repo8 = InMemoryJobRepository()
    app.dependency_overrides[get_job_repo] = lambda: _repo8
    _repo8.create("running-job")
    _repo8.set_status("running-job", JobStatus.running)
    r8 = client.get("/tournaments/running-job/report")
    if r8.status_code != 425:
        print(f"❌ Report for running job should be 425, got {r8.status_code}")
        raise SystemExit(1)
    print("✓ GET report for running job → 425")

    # restore SyncWorker for pytest gate
    app.dependency_overrides[get_job_repo] = lambda: _repo
    app.dependency_overrides[get_worker] = lambda: _worker

    # ── Gate 9: at least 6 test functions ────────────────────────────────────
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

    # ── Gate 10: pytest test_api.py ──────────────────────────────────────────
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

    # ── Gate 11: ProcessPoolTournamentWorker — pickle safety + real parallelism
    #
    # Catches four failure modes:
    #   (a) pool worker function is not picklable (lambda/closure) → PicklingError
    #   (b) submit() still accepts fn: Callable instead of battles: int
    #   (c) ProcessPoolExecutor present in code but job never completes correctly
    #   (d) lambda present inside ProcessPoolTournamentWorker (any lambda is not picklable)
    #
    from jobs.jobs import ProcessPoolTournamentWorker, _simulate_one

    # (a) _simulate_one must be picklable — it is sent to worker processes
    try:
        pickle.dumps(_simulate_one)
    except Exception as e:
        print(f"❌ _simulate_one is not picklable: {e}")
        print("   Hint: keep it as a top-level module function, never a lambda or nested def")
        raise SystemExit(1)
    print("✓ _simulate_one is picklable (safe to send to worker processes)")

    # (b) Worker.submit must accept (job_id, battles: int) — not a Callable
    sig = inspect.signature(ProcessPoolTournamentWorker.submit)
    params = list(sig.parameters.keys())  # ['self', 'job_id', ...]
    if "fn" in params or "callable" in params:
        print("❌ ProcessPoolTournamentWorker.submit still accepts fn/callable")
        print("   It must accept (job_id, battles: int) and distribute battles itself")
        raise SystemExit(1)
    if "battles" not in params:
        print(f"❌ ProcessPoolTournamentWorker.submit should have 'battles' parameter, got: {params}")
        raise SystemExit(1)
    print("✓ ProcessPoolTournamentWorker.submit(job_id, battles) — no lambda/callable")

    # (c) ProcessPoolTournamentWorker actually runs and completes correctly
    _pp_repo = InMemoryJobRepository()
    _pp_worker = ProcessPoolTournamentWorker(_pp_repo, workers=2)
    _pp_repo.create("pp-test")
    _pp_worker.submit("pp-test", 40)

    _deadline = time.monotonic() + 30
    while time.monotonic() < _deadline:
        j = _pp_repo.get("pp-test")
        if j and j.status in (JobStatus.completed, JobStatus.failed):
            break
        time.sleep(0.2)

    j = _pp_repo.get("pp-test")
    if not j or j.status == JobStatus.failed:
        err = j.error if j else "job not found"
        print(f"❌ ProcessPoolTournamentWorker failed: {err}")
        print("   Common cause: pickling error (lambda or closure passed to pool)")
        raise SystemExit(1)
    if j.status != JobStatus.completed:
        print("❌ ProcessPoolTournamentWorker did not complete within 30s")
        raise SystemExit(1)
    if j.result.get("total_battles") != 40:
        print(f"❌ Expected total_battles=40, got: {j.result}")
        raise SystemExit(1)
    print(f"✓ ProcessPoolTournamentWorker completed 40 battles across processes: {j.result}")

    # (d) No lambda inside ProcessPoolTournamentWorker — lambdas are not picklable
    # Note: both pool.map(fn, seeds) and pool.submit(fn, seed) per battle are valid
    # patterns. We do not require one specific API; we only reject lambdas.
    _jobs_src = (project / "jobs" / "jobs.py").read_text(encoding="utf-8")
    _jobs_tree = _ast.parse(_jobs_src)
    for _node in _ast.walk(_jobs_tree):
        if isinstance(_node, _ast.ClassDef) and _node.name == "ProcessPoolTournamentWorker":
            for _child in _ast.walk(_node):
                if isinstance(_child, _ast.Lambda):
                    print("❌ ProcessPoolTournamentWorker contains a lambda — not picklable")
                    print("   Use a module-level function reference (e.g. _simulate_one)")
                    raise SystemExit(1)
    print("✓ ProcessPoolTournamentWorker contains no lambda — pickle-safe")

    update_progress("03_concurrent_tournament_runner")
    print()
    print("✅ Boss fight complete! Concurrent Tournament Runner operational.")
    print("   POST /tournaments ✓  job tracking ✓  Markdown reports ✓  tests ✓")
    print("   ProcessPoolExecutor ✓  real parallel distribution ✓  pickle-safe ✓")
