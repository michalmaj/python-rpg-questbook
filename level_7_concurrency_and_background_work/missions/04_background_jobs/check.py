"""Check: Mission 04 — Background Jobs."""
import json
import sys
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

# ── POST /tournaments → 202 ────────────────────────────────────────────────────
r = client.post("/tournaments", json={"battles": 20})
if r.status_code != 202:
    print(f"❌ POST /tournaments should return 202, got {r.status_code}: {r.text[:200]}")
    raise SystemExit(1)
job_id = r.json().get("job_id")
if not job_id:
    print("❌ Response missing job_id")
    raise SystemExit(1)
print(f"✓ POST /tournaments → 202, job_id={job_id[:8]}...")

# ── GET /jobs/{job_id} → pending or running ────────────────────────────────────
r = client.get(f"/jobs/{job_id}")
if r.status_code != 200:
    print(f"❌ GET /jobs/{job_id} → {r.status_code}")
    raise SystemExit(1)
status = r.json().get("status")
if status not in ("pending", "running", "completed"):
    print(f"❌ Unexpected status: {status}")
    raise SystemExit(1)
print(f"✓ GET /jobs/{job_id} → status={status}")

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
