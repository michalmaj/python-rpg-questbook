# level_6_api/missions/05_dependencies_and_repositories/check.py
"""Check: Mission 05 — Dependencies and Repositories."""
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

# ── dependencies.py exists ────────────────────────────────────────────────────

deps_file = mission / "task/dependencies.py"
if not deps_file.exists():
    print("❌ task/dependencies.py not found — create it with get_battle_service() and get_session_repo()")
    raise SystemExit(1)
deps_src = deps_file.read_text()

for fn in ("get_battle_service", "get_session_repo", "get_monster_repo"):
    if fn not in deps_src:
        print(f"❌ task/dependencies.py: function '{fn}' not found")
        raise SystemExit(1)
print("✓ task/dependencies.py has get_monster_repo, get_session_repo, get_battle_service")

# ── Depends() used in at least one router ────────────────────────────────────

depends_count = 0
for router_file in (mission / "task/routers").glob("*.py"):
    src = router_file.read_text()
    if "Depends(" in src and not all(ln.lstrip().startswith("#") for ln in src.splitlines() if "Depends(" in ln):
        depends_count += 1

if depends_count == 0:
    print("❌ Depends() not used in any router file — refactor endpoints to use Depends(get_battle_service)")
    raise SystemExit(1)
print(f"✓ Depends() used in {depends_count} router file(s)")

# ── no manual instantiation in routers (smell-removal check) ─────────────────

_smell_patterns = ("MonsterRepository(", "BattleService(")
_router_files = (
    mission / "task/routers/monsters.py",
    mission / "task/routers/battles.py",
    mission / "task/routers/sessions.py",
)

for _router_path in _router_files:
    if not _router_path.exists():
        continue
    _rel = f"task/routers/{_router_path.name}"
    for _line in _router_path.read_text().splitlines():
        if _line.lstrip().startswith("#"):
            continue
        for _pattern in _smell_patterns:
            if _pattern in _line:
                print(
                    f"❌ {_rel}: '{_pattern}' found outside comments — "
                    "use Depends() instead of instantiating manually"
                )
                raise SystemExit(1)

print("✓ No manual MonsterRepository()/BattleService() instantiation in routers")

# ── functional: existing endpoints still work ────────────────────────────────

try:
    from task.main import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import app from task.main: {exc}")
    raise SystemExit(1)

from fastapi.testclient import TestClient

client = TestClient(app)

r = client.get("/monsters")
if r.status_code != 200 or not r.json():
    print(f"❌ GET /monsters broke: {r.status_code}")
    raise SystemExit(1)
print("✓ GET /monsters → 200")

r = client.post(
    "/battle/simulate",
    json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"},
)
if r.status_code != 200:
    print(f"❌ POST /battle/simulate returned {r.status_code}: {r.text[:200]}")
    raise SystemExit(1)
print("✓ POST /battle/simulate → 200")

# ── POST /sessions ────────────────────────────────────────────────────────────

r = client.post(
    "/sessions",
    json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"},
)
if r.status_code != 201:
    print(f"❌ POST /sessions returned {r.status_code} (expected 201): {r.text[:200]}")
    raise SystemExit(1)
if "session_id" not in r.json():
    print("❌ POST /sessions response missing 'session_id'")
    raise SystemExit(1)
session_id = r.json()["session_id"]
print(f"✓ POST /sessions → 201, session_id={session_id[:8]}...")

# ── GET /sessions/{session_id} ────────────────────────────────────────────────

r = client.get(f"/sessions/{session_id}")
if r.status_code != 200:
    print(f"❌ GET /sessions/{'{id}'} returned {r.status_code}: {r.text[:200]}")
    raise SystemExit(1)
if "winner" not in r.json():
    print("❌ GET /sessions/{id} response missing 'winner' field")
    raise SystemExit(1)
print("✓ GET /sessions/{id} → 200")

r = client.get("/sessions/nonexistent-id-12345")
if r.status_code != 404:
    print(f"❌ GET /sessions/nonexistent should return 404, got {r.status_code}")
    raise SystemExit(1)
print("✓ GET /sessions/nonexistent → 404")

update_progress("05_dependencies_and_repositories")
print("\n✅ Mission 05 complete!")
