"""check.py — Project 02: Background Report Queue"""

import ast
import json
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[3] / "level_7_concurrency_and_background_work" / ".progress"

sys.path.insert(0, str(PROJECT_DIR))


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


def main() -> None:
    # ── 1. Import app ─────────────────────────────────────────────────────────
    try:
        from task.main import app
    except ImportError as exc:
        print(f"❌ Cannot import app from task.main: {exc}")
        raise SystemExit(1)
    except Exception as exc:
        print(f"❌ Error loading task.main: {exc}")
        raise SystemExit(1)

    import warnings
    warnings.filterwarnings("ignore")
    from fastapi.testclient import TestClient

    from task.dependencies import get_repo, get_worker
    from task.jobs import InMemoryJobRepository, SyncWorker

    # ── Wire up SyncWorker for deterministic testing ──────────────────────────
    _repo = InMemoryJobRepository()
    _worker = SyncWorker(_repo)
    app.dependency_overrides[get_repo] = lambda: _repo
    app.dependency_overrides[get_worker] = lambda: _worker

    client = TestClient(app, raise_server_exceptions=False)

    # ── 2. Scaffold guard: submit must be implemented ─────────────────────────
    r = client.post("/reports", json={"label": "test"})
    if r.status_code == 500:
        print("❌ BackgroundWorker.submit() is not implemented yet")
        print("   Implement the method in task/jobs.py — see the docstring for requirements")
        raise SystemExit(1)

    # ── 3. GET /health ────────────────────────────────────────────────────────
    r = client.get("/health")
    if r.status_code != 200:
        print(f"❌ GET /health returned {r.status_code}")
        raise SystemExit(1)
    print("✓ GET /health → 200")

    # ── 4. POST /reports → 202 + job_id ──────────────────────────────────────
    r = client.post("/reports", json={"label": "combat_report"})
    if r.status_code != 202:
        print(f"❌ POST /reports should return 202, got {r.status_code}: {r.text[:300]}")
        raise SystemExit(1)
    job_id = r.json().get("job_id")
    if not job_id:
        print("❌ POST /reports response missing 'job_id' field")
        raise SystemExit(1)
    print(f"✓ POST /reports → 202, job_id={job_id[:8]}...")

    # ── 5. GET /reports/{job_id} → completed with correct result fields ───────
    r = client.get(f"/reports/{job_id}")
    if r.status_code != 200:
        print(f"❌ GET /reports/{job_id} → {r.status_code}")
        raise SystemExit(1)
    data = r.json()
    if data.get("status") != "completed":
        print(f"❌ Job should be 'completed' (SyncWorker runs inline), got '{data.get('status')}'")
        raise SystemExit(1)
    result = data.get("result")
    if not result:
        print("❌ Job result is empty after completion")
        raise SystemExit(1)
    for field in ("total_sessions", "hero_win_rate", "markdown"):
        if field not in result:
            print(f"❌ result missing field '{field}'")
            raise SystemExit(1)
    if result["total_sessions"] != 5:
        print(f"❌ total_sessions should be 5 (5 JSON files), got {result['total_sessions']}")
        raise SystemExit(1)
    if "# Combat Report" not in result["markdown"]:
        print("❌ result.markdown should contain '# Combat Report'")
        raise SystemExit(1)
    print(
        f"✓ GET /reports/{job_id[:8]}... → completed, "
        f"total_sessions={result['total_sessions']}, "
        f"hero_win_rate={result['hero_win_rate']}"
    )

    # ── 6. hero_win_rate is correct (3 hero wins out of 5) ───────────────────
    expected_rate = round(3 / 5, 4)
    if abs(result["hero_win_rate"] - expected_rate) > 0.001:
        print(f"❌ hero_win_rate should be {expected_rate} (3/5 sessions), got {result['hero_win_rate']}")
        raise SystemExit(1)
    print(f"✓ hero_win_rate={result['hero_win_rate']} (3 hero wins / 5 sessions = 0.6)")

    # ── 7. GET /reports/{nonexistent} → 404 ──────────────────────────────────
    r = client.get("/reports/nonexistent-job-xyz")
    if r.status_code != 404:
        print(f"❌ Unknown job_id should return 404, got {r.status_code}")
        raise SystemExit(1)
    print("✓ GET /reports/nonexistent → 404")

    # ── 8. Invalid body → 422 ────────────────────────────────────────────────
    r = client.post("/reports", json={"label": 123})
    # label=123 (int instead of str) — Pydantic coerces it, which is fine.
    # An actually invalid body (missing required fields on a strict schema) is hard to trigger
    # for a model with all-optional fields, so we test that unknown extra fields are OK too.
    # The real 422 gate: send non-JSON body.
    r = client.post("/reports", content=b"not-json", headers={"content-type": "application/json"})
    if r.status_code != 422:
        print(f"❌ Malformed JSON body should return 422, got {r.status_code}")
        raise SystemExit(1)
    print("✓ Malformed JSON body → 422")

    # ── 9. AST: BackgroundWorker + SyncWorker both defined in jobs.py ─────────
    jobs_src = (PROJECT_DIR / "task" / "jobs.py").read_text(encoding="utf-8")
    jobs_tree = ast.parse(jobs_src)
    class_names = {n.name for n in ast.walk(jobs_tree) if isinstance(n, ast.ClassDef)}
    for cls in ("BackgroundWorker", "SyncWorker"):
        if cls not in class_names:
            print(f"❌ {cls} class not found in task/jobs.py")
            raise SystemExit(1)
    print("✓ BackgroundWorker and SyncWorker both defined in task/jobs.py")

    # ── 10. AST: BackgroundWorker.submit uses threading.Thread ───────────────
    _found_thread = False
    for node in ast.walk(jobs_tree):
        if not isinstance(node, ast.ClassDef) or node.name != "BackgroundWorker":
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and child.id == "Thread":
                _found_thread = True
            if isinstance(child, ast.Attribute) and child.attr == "Thread":
                _found_thread = True
    if not _found_thread:
        print("❌ BackgroundWorker must use threading.Thread to run jobs in the background")
        raise SystemExit(1)
    print("✓ BackgroundWorker uses threading.Thread")

    # ── 11. Behavioural: BackgroundWorker actually runs in a background thread ─
    import threading as _threading

    from task.jobs import BackgroundWorker as _BW

    _bw_repo = InMemoryJobRepository()
    _bw = _BW(_bw_repo)
    _bw_job = _bw_repo.create()

    _started = _threading.Event()
    _release = _threading.Event()

    def _blocking_task() -> dict:
        _started.set()
        _release.wait(timeout=5)
        return {
            "total_sessions": 1, "hero_wins": 1, "monster_wins": 0,
            "hero_win_rate": 1.0, "avg_damage_dealt": 10.0,
            "avg_damage_taken": 5.0, "markdown": "# test",
        }

    import time as _time
    _t0 = _time.monotonic()
    _bw.submit(_bw_job.job_id, _blocking_task)
    _submit_elapsed = _time.monotonic() - _t0

    if _submit_elapsed > 0.1:
        _release.set()
        print(f"❌ BackgroundWorker.submit() took {_submit_elapsed:.3f}s — must return immediately")
        raise SystemExit(1)

    if not _started.wait(timeout=2):
        _release.set()
        print("❌ BackgroundWorker: task never started — thread was not launched")
        raise SystemExit(1)

    _mid_state = _bw_repo.get(_bw_job.job_id)
    if _mid_state is None or _mid_state.status != "running":
        _release.set()
        status = _mid_state.status if _mid_state else "None"
        print(f"❌ BackgroundWorker: status should be 'running' while task executes, got '{status}'")
        raise SystemExit(1)

    _release.set()
    _time.sleep(0.15)

    _final_state = _bw_repo.get(_bw_job.job_id)
    if _final_state is None or _final_state.status != "completed":
        status = _final_state.status if _final_state else "None"
        print(f"❌ BackgroundWorker: status should be 'completed' after task, got '{status}'")
        raise SystemExit(1)
    if not _final_state.result:
        print("❌ BackgroundWorker: result is empty after task completed")
        raise SystemExit(1)

    print(f"✓ BackgroundWorker: submit returns in {_submit_elapsed:.3f}s, "
          f"task runs in background, status → running → completed")

    # exception path: failed status
    _err_repo = InMemoryJobRepository()
    _err_worker = _BW(_err_repo)
    _err_job = _err_repo.create()

    def _failing_task() -> dict:
        raise ValueError("expected failure")

    _err_worker.submit(_err_job.job_id, _failing_task)
    _time.sleep(0.15)

    _err_state = _err_repo.get(_err_job.job_id)
    if _err_state is None or _err_state.status != "failed":
        status = _err_state.status if _err_state else "None"
        print(f"❌ BackgroundWorker: exception should set status to 'failed', got '{status}'")
        raise SystemExit(1)
    print("✓ BackgroundWorker: exceptions correctly set status to 'failed'")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("02_background_report_queue")
    print()
    print("✅ Project 02 complete: Background Report Queue works!")
    print()
    print("   POST /reports enqueues the job immediately (202).")
    print("   GET /reports/{id} returns live status + result when done.")
    print("   daemon threads = API stays responsive during heavy computation.")


if __name__ == "__main__":
    main()
