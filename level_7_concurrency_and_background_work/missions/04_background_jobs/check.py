"""Check: Mission 04 — Background Jobs."""
import json
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
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


try:
    from task.main import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import app: {exc}")
    raise SystemExit(1)

import warnings
warnings.filterwarnings("ignore")
from fastapi.testclient import TestClient

client = TestClient(app, raise_server_exceptions=False)

# ── Behavioral proof: POST must return BEFORE the tournament finishes ────────
#
# A synchronous "fake background job" (run the whole tournament inline, then
# fabricate a completed job entry) returns 202 with a real job_id too — the
# only way to tell it apart from real background execution is to block the
# actual simulation and confirm the HTTP response comes back anyway.
#
# _svc.simulate_tournament is the one call every correct implementation must
# make (directly or via the given _run_tournament helper) to produce a real
# result — so it's the right seam to block on, regardless of how the student
# wires the background thread.

import task.routers.tournaments as _tourn_mod  # type: ignore[import]

if not hasattr(_tourn_mod, "_svc"):
    print("❌ task/routers/tournaments.py: expected module-level _svc (SimulationService) not found")
    raise SystemExit(1)

_worker_started = threading.Event()
_allow_finish = threading.Event()
_original_simulate = _tourn_mod._svc.simulate_tournament


def _blocking_simulate(n: int):
    _worker_started.set()
    _allow_finish.wait(timeout=10)
    return _original_simulate(n)


_post_result: dict = {}


def _do_post() -> None:
    try:
        _post_result["response"] = client.post("/tournaments", json={"battles": 20})
    except Exception as exc:  # pragma: no cover - surfaced via _post_result
        _post_result["error"] = exc


_tourn_mod._svc.simulate_tournament = _blocking_simulate
_post_thread = threading.Thread(target=_do_post, daemon=True)

try:
    _post_thread.start()

    if not _worker_started.wait(timeout=5):
        print("❌ simulate_tournament was never called — POST /tournaments did not start the simulation")
        raise SystemExit(1)

    # The worker is now blocked on _allow_finish. A real background
    # implementation must have already returned the HTTP response by now.
    _post_thread.join(timeout=2)
    if _post_thread.is_alive():
        print("❌ POST /tournaments did not return while the tournament was still running.")
        print("   This means the simulation runs synchronously inside the request,")
        print("   not in the background — that defeats the whole point of this mission.")
        raise SystemExit(1)

    if "error" in _post_result:
        print(f"❌ POST /tournaments raised: {_post_result['error']}")
        raise SystemExit(1)

    r = _post_result["response"]
    if r.status_code != 202:
        print(f"❌ POST /tournaments should return 202, got {r.status_code}: {r.text[:200]}")
        raise SystemExit(1)
    job_id = r.json().get("job_id")
    if not job_id:
        print("❌ Response missing job_id")
        raise SystemExit(1)
    print(f"✓ POST /tournaments → 202 while the worker was still blocked — truly background. job_id={job_id[:8]}...")

    # ── status while the worker is still blocked ─────────────────────────────
    r = client.get(f"/jobs/{job_id}")
    if r.status_code != 200:
        print(f"❌ GET /jobs/{job_id} → {r.status_code}")
        raise SystemExit(1)
    status = r.json().get("status")
    if status not in ("pending", "running"):
        print(f"❌ Job should still be pending/running while blocked, got '{status}'")
        raise SystemExit(1)
    print(f"✓ GET /jobs/{job_id} → status={status} (while worker still blocked)")
finally:
    _allow_finish.set()
    _post_thread.join(timeout=5)
    _tourn_mod._svc.simulate_tournament = _original_simulate

if _post_thread.is_alive():
    print("❌ internal check error: background POST thread did not finish during cleanup")
    raise SystemExit(1)

# ── poll until completed (timeout 10s) ────────────────────────────────────────
deadline = time.time() + 10
while time.time() < deadline:
    r = client.get(f"/jobs/{job_id}")
    if r.json().get("status") == "completed":
        break
    time.sleep(0.1)
else:
    print("❌ Job did not complete within 10 seconds")
    raise SystemExit(1)
result = r.json().get("result")
if not result or result.get("total_battles") != 20:
    print(f"❌ Job result missing or wrong: {result}")
    raise SystemExit(1)
print(f"✓ Job completed: {result}")

# ── unknown job → 404 ─────────────────────────────────────────────────────────
r = client.get("/jobs/nonexistent-job-xyz")
if r.status_code != 404:
    print(f"❌ Unknown job should be 404, got {r.status_code}")
    raise SystemExit(1)
print("✓ GET /jobs/unknown → 404")

# ── invalid battles → 422 ─────────────────────────────────────────────────────
r = client.post("/tournaments", json={"battles": 0})
if r.status_code != 422:
    print(f"❌ battles=0 should return 422, got {r.status_code}")
    raise SystemExit(1)
print("✓ POST /tournaments with battles=0 → 422")

update_progress("04_background_jobs")
print("\n✅ Mission 04 complete! You built the job-id pattern.")
