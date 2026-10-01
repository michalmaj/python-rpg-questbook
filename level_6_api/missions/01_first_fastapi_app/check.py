# level_6_api/missions/01_first_fastapi_app/check.py
"""Check: Mission 01 — First FastAPI App."""
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


# ── import app ────────────────────────────────────────────────────────────────

try:
    from task import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import 'app' from task.py: {exc}")
    print("   Make sure you defined: app = FastAPI(...)")
    raise SystemExit(1)

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except ImportError:
    print("❌ fastapi not installed — run: uv sync")
    raise SystemExit(1)

if not isinstance(app, FastAPI):
    print("❌ 'app' must be a FastAPI instance (app = FastAPI(...))")
    raise SystemExit(1)
print("✓ app is a FastAPI instance")

client = TestClient(app)

# ── GET /health ───────────────────────────────────────────────────────────────

r = client.get("/health")
if r.status_code != 200:
    print(f"❌ GET /health returned {r.status_code} (expected 200)")
    raise SystemExit(1)
body = r.json()
if not isinstance(body, dict) or "status" not in body:
    print("❌ GET /health must return JSON with a 'status' field")
    raise SystemExit(1)
print("✓ GET /health → 200 with 'status' field")

# ── GET /monsters ─────────────────────────────────────────────────────────────
#
# Not just "non-empty" — the names must actually match data/monsters.json.
# A hardcoded list that never calls the service would pass a length-only check.

r = client.get("/monsters")
if r.status_code != 200:
    print(f"❌ GET /monsters returned {r.status_code} (expected 200)")
    raise SystemExit(1)
data = r.json()
if not isinstance(data, list) or len(data) == 0:
    print("❌ GET /monsters must return a non-empty list")
    raise SystemExit(1)
if not all(isinstance(item, str) for item in data):
    print(f"❌ GET /monsters must return a list of strings, got {data!r}")
    raise SystemExit(1)

real_data = json.loads((Path(__file__).parent / "data" / "monsters.json").read_text())
expected_names = {m["name"] for m in real_data["monsters"]}
returned_names = set(data)
if returned_names != expected_names:
    print(f"❌ GET /monsters returned {sorted(returned_names)}, "
          f"but data/monsters.json actually has {sorted(expected_names)}")
    print("   Return the real monster names from _service.get_available_monsters(), "
          "not a hardcoded list.")
    raise SystemExit(1)
print(f"✓ GET /monsters → 200, {len(data)} monsters matching data/monsters.json")

update_progress("01_first_fastapi_app")
print("\n✅ Mission 01 complete!")
