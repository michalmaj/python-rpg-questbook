# level_6_api/projects/01_rpg_battle_api/check.py
"""Check: Boss Fight — RPG Battle API."""
import json
import subprocess
import sys
from pathlib import Path

project = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[2] / ".progress"


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


print("Checking boss fight: rpg_battle_api")
print("=" * 50)

# ── Gate 1: import app ────────────────────────────────────────────────────────

sys.path.insert(0, str(project))
try:
    from rpg.api.main import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import app from rpg.api.main: {exc}")
    raise SystemExit(1)

from fastapi.testclient import TestClient
from rpg.api.dependencies import get_session_repo  # type: ignore[import]
from rpg.repositories import SessionRepository  # type: ignore[import]

import tempfile
_tmp = tempfile.mkdtemp()
app.dependency_overrides[get_session_repo] = lambda: SessionRepository(Path(_tmp))
client = TestClient(app, raise_server_exceptions=False)

# ── Gate 2: GET /health ───────────────────────────────────────────────────────

r = client.get("/health")
if r.status_code != 200:
    print(f"❌ GET /health returned {r.status_code}")
    raise SystemExit(1)
print("✓ GET /health → 200")

# ── Gate 3: GET /monsters ─────────────────────────────────────────────────────

r = client.get("/monsters")
if r.status_code != 200 or not r.json():
    print(f"❌ GET /monsters returned {r.status_code}: {r.text[:200]}")
    raise SystemExit(1)
print(f"✓ GET /monsters → 200, {len(r.json())} monsters")

# ── Gate 4: GET /heroes/classes ───────────────────────────────────────────────

r = client.get("/heroes/classes")
if r.status_code != 200 or not r.json():
    print(f"❌ GET /heroes/classes returned {r.status_code}")
    raise SystemExit(1)
print(f"✓ GET /heroes/classes → 200, {len(r.json())} classes")

# ── Gate 5: POST /battle/simulate ────────────────────────────────────────────

r = client.post(
    "/battle/simulate",
    json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"},
)
if r.status_code != 200:
    print(f"❌ POST /battle/simulate returned {r.status_code}: {r.text[:300]}")
    raise SystemExit(1)
if "winner" not in r.json():
    print("❌ POST /battle/simulate response missing 'winner'")
    raise SystemExit(1)
print("✓ POST /battle/simulate → 200, winner present")

# ── Gate 6: POST /sessions → 201 + session_id ────────────────────────────────

r = client.post(
    "/sessions",
    json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"},
)
if r.status_code != 201:
    print(f"❌ POST /sessions returned {r.status_code} (expected 201): {r.text[:200]}")
    raise SystemExit(1)
session_id = r.json().get("session_id")
if not session_id:
    print("❌ POST /sessions response missing 'session_id'")
    raise SystemExit(1)
print(f"✓ POST /sessions → 201, session_id={session_id[:8]}...")

# ── Gate 7: GET /sessions/{id} ────────────────────────────────────────────────

r = client.get(f"/sessions/{session_id}")
if r.status_code != 200:
    print(f"❌ GET /sessions/{{id}} returned {r.status_code}")
    raise SystemExit(1)
print("✓ GET /sessions/{id} → 200")

r = client.get("/sessions/nonexistent-xyz-00000")
if r.status_code != 404:
    print(f"❌ GET /sessions/nonexistent should be 404, got {r.status_code}")
    raise SystemExit(1)
print("✓ GET /sessions/nonexistent → 404")

# ── Gate 8: GET /reports/{id} ────────────────────────────────────────────────

r = client.get(f"/reports/{session_id}")
if r.status_code != 200:
    print(f"❌ GET /reports/{{id}} returned {r.status_code}: {r.text[:200]}")
    raise SystemExit(1)
body = r.text if isinstance(r.text, str) else str(r.json())
if "##" not in body and "#" not in body:
    print("❌ GET /reports/{id} response should contain Markdown (## header)")
    raise SystemExit(1)
print("✓ GET /reports/{id} → 200, Markdown content")

# ── Gate 9: pytest test_api.py ────────────────────────────────────────────────

app.dependency_overrides.clear()

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_api.py", "-q", "--tb=short"],
    capture_output=True,
    text=True,
    cwd=str(project),
)
if result.returncode != 0:
    print("❌ pytest tests/test_api.py fails:")
    print(result.stdout[-2000:])
    raise SystemExit(1)
print("✓ All API tests pass")

update_progress("01_rpg_battle_api")
print()
print("✅ Boss fight complete! RPG Battle API fully operational.")
print("   7 endpoints ✓  session persistence ✓  Markdown reports ✓  tests ✓")
