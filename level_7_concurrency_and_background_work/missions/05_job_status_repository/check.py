"""Check: Mission 05 — Job Status Repository."""
import json
import sys
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


# ── InMemoryJobRepository unit tests ─────────────────────────────────────────
try:
    from task.jobs import InMemoryJobRepository, JobStatus  # type: ignore
except ImportError as exc:
    print(f"❌ Cannot import from task.jobs: {exc}")
    raise SystemExit(1)

repo = InMemoryJobRepository()
job = repo.create("test-job-1")
if job.status != JobStatus.pending:
    print(f"❌ New job should be pending, got {job.status}")
    raise SystemExit(1)
repo.set_status("test-job-1", JobStatus.running)
job = repo.get("test-job-1")
if job.status != JobStatus.running:
    print(f"❌ Status should be running, got {job.status}")
    raise SystemExit(1)
repo.set_result("test-job-1", {"total_battles": 5})
repo.set_status("test-job-1", JobStatus.completed)
job = repo.get("test-job-1")
if job.status != JobStatus.completed or job.result != {"total_battles": 5}:
    print(f"❌ Job not completed correctly: {job}")
    raise SystemExit(1)
if repo.get("nonexistent") is not None:
    print("❌ get() should return None for nonexistent job")
    raise SystemExit(1)
print("✓ InMemoryJobRepository: create/get/set_status/set_result work correctly")

# ── JsonJobRepository unit tests ─────────────────────────────────────────────
import tempfile
try:
    from task.jobs import JsonJobRepository  # type: ignore
except ImportError as exc:
    print(f"❌ Cannot import JsonJobRepository: {exc}")
    raise SystemExit(1)

with tempfile.TemporaryDirectory() as tmp:
    jrepo = JsonJobRepository(Path(tmp))
    job = jrepo.create("json-job-1")
    jrepo.set_status("json-job-1", JobStatus.completed)
    jrepo.set_result("json-job-1", {"total_battles": 10})
    loaded = jrepo.get("json-job-1")
    if loaded is None or loaded.status != JobStatus.completed:
        print(f"❌ JsonJobRepository did not persist correctly: {loaded}")
        raise SystemExit(1)
print("✓ JsonJobRepository persists jobs to disk")

# ── SyncWorker unit test ──────────────────────────────────────────────────────
try:
    from task.workers import SyncWorker  # type: ignore
except ImportError as exc:
    print(f"❌ Cannot import SyncWorker: {exc}")
    raise SystemExit(1)

repo2 = InMemoryJobRepository()
worker = SyncWorker(repo2)
repo2.create("sync-job-1")
worker.submit("sync-job-1", lambda: {"result": 42})
job = repo2.get("sync-job-1")
if job.status != JobStatus.completed or job.result != {"result": 42}:
    print(f"❌ SyncWorker did not complete job correctly: {job}")
    raise SystemExit(1)
print("✓ SyncWorker runs job inline, sets completed status")

# ── API integration (using SyncWorker for determinism — no time.sleep) ────────
try:
    from task.main import app  # type: ignore
    from task.dependencies import get_job_repo, get_worker  # type: ignore
except ImportError as exc:
    print(f"❌ Cannot import app or dependencies: {exc}")
    raise SystemExit(1)

import warnings
warnings.filterwarnings("ignore")
from fastapi.testclient import TestClient

check_repo = InMemoryJobRepository()
check_worker = SyncWorker(check_repo)
app.dependency_overrides[get_job_repo] = lambda: check_repo
app.dependency_overrides[get_worker] = lambda: check_worker

client = TestClient(app, raise_server_exceptions=False)
BATTLES = 20
r = client.post("/tournaments", json={"battles": BATTLES})
if r.status_code != 202:
    print(f"❌ POST /tournaments should return 202, got {r.status_code}")
    app.dependency_overrides.clear()
    raise SystemExit(1)
job_id = r.json().get("job_id")

# SyncWorker runs inline — job is already completed after POST returns
r = client.get(f"/jobs/{job_id}")
if r.json().get("status") != "completed":
    print(f"❌ Job should be completed immediately with SyncWorker, got {r.json().get('status')}")
    app.dependency_overrides.clear()
    raise SystemExit(1)

# The result must reflect the actual tournament that ran — not just any dict
# that happens to make the status look "completed". total_battles is
# deterministic (it's the request's battles count); hero_wins/monster_wins
# are random per-battle, so only their sum (not exact values) is checked.
result = r.json().get("result")
if not isinstance(result, dict):
    print(f"❌ Job result should be a dict, got {result!r}")
    app.dependency_overrides.clear()
    raise SystemExit(1)
if result.get("total_battles") != BATTLES:
    print(f"❌ result['total_battles'] should be {BATTLES}, got {result.get('total_battles')!r}")
    print("   The result must come from the real simulate_tournament() call, not a fabricated dict.")
    app.dependency_overrides.clear()
    raise SystemExit(1)
hero_wins = result.get("hero_wins")
monster_wins = result.get("monster_wins")
if not isinstance(hero_wins, int) or not isinstance(monster_wins, int) or hero_wins + monster_wins != BATTLES:
    print(f"❌ result hero_wins ({hero_wins!r}) + monster_wins ({monster_wins!r}) should equal {BATTLES}")
    app.dependency_overrides.clear()
    raise SystemExit(1)
print(f"✓ API: POST /tournaments → 202, job completes instantly (SyncWorker), "
      f"result matches the real simulation: {result}")

r = client.get("/jobs/nonexistent")
if r.status_code != 404:
    print(f"❌ Unknown job should be 404, got {r.status_code}")
    app.dependency_overrides.clear()
    raise SystemExit(1)
print("✓ GET /jobs/unknown → 404")

app.dependency_overrides.clear()

# ── no global _jobs dict in routers ──────────────────────────────────────────
router_src = (Path(__file__).parent / "task" / "routers" / "tournaments.py").read_text()
code_lines = [ln for ln in router_src.splitlines() if not ln.lstrip().startswith("#")]
if "_jobs" in "\n".join(code_lines):
    print("❌ Router still uses global _jobs dict — refactor to use JobRepository")
    raise SystemExit(1)
print("✓ No global _jobs dict in router — clean JobRepository usage")

update_progress("05_job_status_repository")
print("\n✅ Mission 05 complete! JobRepository Pattern applied.")
