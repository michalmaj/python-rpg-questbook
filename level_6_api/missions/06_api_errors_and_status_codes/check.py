# level_6_api/missions/06_api_errors_and_status_codes/check.py
"""Check: Mission 06 — API Errors and Status Codes."""
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


mission = Path(__file__).parent

# ── ErrorOut schema defined ───────────────────────────────────────────────────

schemas_file = mission / "task/schemas.py"
routers_dir = mission / "task/routers"

error_out_found = False
if schemas_file.exists() and "class ErrorOut" in schemas_file.read_text():
    error_out_found = True
else:
    for f in routers_dir.glob("*.py"):
        if "class ErrorOut" in f.read_text():
            error_out_found = True
            break

if not error_out_found:
    print("❌ ErrorOut schema not found — create it in task/schemas.py")
    raise SystemExit(1)
print("✓ ErrorOut schema defined")

# ── HTTPException used ────────────────────────────────────────────────────────

http_exc_count = sum(
    1 for f in routers_dir.glob("*.py")
    if "HTTPException" in f.read_text()
    and any(
        "HTTPException" in ln and not ln.lstrip().startswith("#")
        for ln in f.read_text().splitlines()
    )
)
if http_exc_count == 0:
    print("❌ HTTPException not used in any router file")
    raise SystemExit(1)
print(f"✓ HTTPException used in {http_exc_count} router file(s)")

# ── functional tests ──────────────────────────────────────────────────────────

try:
    from task.main import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import app from task.main: {exc}")
    raise SystemExit(1)

from fastapi.testclient import TestClient

client = TestClient(app, raise_server_exceptions=False)

# unknown monster → 404
r = client.post(
    "/battle/simulate",
    json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "FakeMonster"},
)
if r.status_code != 404:
    print(f"❌ Unknown monster should return 404, got {r.status_code}")
    raise SystemExit(1)
print("✓ POST /battle/simulate with unknown monster → 404")

# known monster → 200
r = client.post(
    "/battle/simulate",
    json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"},
)
if r.status_code != 200:
    print(f"❌ POST /battle/simulate (known monster) returned {r.status_code}")
    raise SystemExit(1)
print("✓ POST /battle/simulate with known monster → 200")

# unknown session → 404
r = client.get("/sessions/nonexistent-abc")
if r.status_code != 404:
    print(f"❌ GET /sessions/nonexistent should be 404, got {r.status_code}")
    raise SystemExit(1)
print("✓ GET /sessions/nonexistent → 404")

# GET /heroes/classes → 200 non-empty list
r = client.get("/heroes/classes")
if r.status_code != 200:
    print(f"❌ GET /heroes/classes returned {r.status_code}")
    raise SystemExit(1)
if not r.json():
    print("❌ GET /heroes/classes returned empty list")
    raise SystemExit(1)
print(f"✓ GET /heroes/classes → 200, {len(r.json())} classes")

# GET /monsters/Goblin → 200 with name key
r = client.get("/monsters/Goblin")
if r.status_code != 200:
    print(f"❌ GET /monsters/Goblin returned {r.status_code}")
    raise SystemExit(1)
if "name" not in r.json():
    print("❌ GET /monsters/Goblin response missing 'name' key")
    raise SystemExit(1)
print("✓ GET /monsters/Goblin → 200")

# GET /monsters/NonExistentMonster → 404
r = client.get("/monsters/NonExistentMonster")
if r.status_code != 404:
    print(f"❌ Unknown monster should return 404, got {r.status_code}")
    raise SystemExit(1)
print("✓ GET /monsters/NonExistentMonster → 404")

update_progress("06_api_errors_and_status_codes")
print("\n✅ Mission 06 complete!")
