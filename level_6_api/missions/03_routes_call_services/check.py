# level_6_api/missions/03_routes_call_services/check.py
"""Check: Mission 03 — Routes Call Services."""
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

# ── combat logic removed from task.py ────────────────────────────────────────

for smell in ("random.randint", "copy.deepcopy"):
    lines_with_smell = [
        ln for ln in src.splitlines()
        if smell in ln and not ln.lstrip().startswith("#")
    ]
    if lines_with_smell:
        print(f"❌ '{smell}' found in task.py — move combat logic into BattleService")
        raise SystemExit(1)
print("✓ No combat logic (random.randint, copy.deepcopy) in task.py")

# ── service.simulate() called ────────────────────────────────────────────────

has_simulate_call = any(
    ".simulate(" in ln and not ln.lstrip().startswith("#")
    for ln in src.splitlines()
)
if not has_simulate_call:
    print("❌ .simulate() not called in task.py — endpoint must call _service.simulate()")
    raise SystemExit(1)
print("✓ _service.simulate() called in endpoint")

# ── create_hero() used (or Hero constructed with correct stats) ───────────────

# Acceptable patterns: create_hero() or Hero(...) with hero_class from request
has_hero_creation = any(
    ("create_hero(" in ln or "Hero(" in ln) and not ln.lstrip().startswith("#")
    for ln in src.splitlines()
)
if not has_hero_creation:
    print("❌ Hero not created — use create_hero(req.hero_name, req.hero_class) from rpg.services")
    raise SystemExit(1)
print("✓ Hero created in endpoint")

# ── endpoints still work ──────────────────────────────────────────────────────

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
print("✓ POST /battle/simulate → 200, BattleResultOut with winner")

r = client.get("/monsters")
if r.status_code != 200 or not r.json():
    print(f"❌ GET /monsters broke: {r.status_code}")
    raise SystemExit(1)
print("✓ GET /monsters still → 200")

update_progress("03_routes_call_services")
print("\n✅ Mission 03 complete!")
