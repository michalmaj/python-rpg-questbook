# level_6_api/missions/02_request_response_schemas/check.py
"""Check: Mission 02 — Request/Response Schemas."""
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


try:
    from task import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import 'app' from task.py: {exc}")
    raise SystemExit(1)

from fastapi.testclient import TestClient

client = TestClient(app)
src = (Path(__file__).parent / "task.py").read_text()

# ── Pydantic schemas defined ──────────────────────────────────────────────────

for schema in ("MonsterOut", "BattleRequest", "BattleResultOut"):
    count = sum(
        1 for ln in src.splitlines()
        if f"class {schema}" in ln and not ln.lstrip().startswith("#")
    )
    if count == 0:
        print(f"❌ Pydantic class '{schema}' not defined in task.py")
        raise SystemExit(1)
print("✓ MonsterOut, BattleRequest, BattleResultOut schemas defined")

# ── GET /monsters returns list of objects with 'name' field ──────────────────

r = client.get("/monsters")
if r.status_code != 200:
    print(f"❌ GET /monsters returned {r.status_code}")
    raise SystemExit(1)
items = r.json()
if not isinstance(items, list) or len(items) == 0:
    print("❌ GET /monsters must return a non-empty list")
    raise SystemExit(1)
if not isinstance(items[0], dict) or "name" not in items[0]:
    print("❌ GET /monsters items must be MonsterOut objects with a 'name' field")
    raise SystemExit(1)
print(f"✓ GET /monsters → 200, {len(items)} MonsterOut objects")

# ── response_model used on /monsters ─────────────────────────────────────────

has_response_model = any(
    "response_model" in ln and "monsters" in ln and not ln.lstrip().startswith("#")
    for ln in src.splitlines()
)
if not has_response_model:
    print("❌ GET /monsters decorator should use response_model=list[MonsterOut]")
    raise SystemExit(1)
print("✓ response_model= used on GET /monsters")

# ── POST /battle/simulate ─────────────────────────────────────────────────────

r = client.post(
    "/battle/simulate",
    json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"},
)
if r.status_code != 200:
    print(f"❌ POST /battle/simulate returned {r.status_code}: {r.text[:300]}")
    raise SystemExit(1)
result = r.json()
for field in ("hero_name", "monster_name", "winner", "rounds", "gold_earned"):
    if field not in result:
        print(f"❌ POST /battle/simulate response missing field '{field}'")
        raise SystemExit(1)
print("✓ POST /battle/simulate → 200, BattleResultOut with all fields")

# ── response_model on /battle/simulate ───────────────────────────────────────

has_sim_rm = any(
    "response_model" in ln and "simulate" in ln and not ln.lstrip().startswith("#")
    for ln in src.splitlines()
)
if not has_sim_rm:
    print("❌ POST /battle/simulate decorator should use response_model=BattleResultOut")
    raise SystemExit(1)
print("✓ response_model= used on POST /battle/simulate")

update_progress("02_request_response_schemas")
print("\n✅ Mission 02 complete!")
