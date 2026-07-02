# level_6_api/missions/04_api_routers/check.py
"""Check: Mission 04 — API Routers."""
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

# ── router files exist ────────────────────────────────────────────────────────

for fname in (
    "task/routers/__init__.py",
    "task/routers/monsters.py",
    "task/routers/battles.py",
):
    if not (mission / fname).exists():
        print(f"❌ {fname} not found — create this file")
        raise SystemExit(1)
print("✓ task/routers/monsters.py and task/routers/battles.py exist")

# ── APIRouter used ────────────────────────────────────────────────────────────

for fname in ("task/routers/monsters.py", "task/routers/battles.py"):
    src = (mission / fname).read_text()
    has_router = any(
        "APIRouter" in ln and not ln.lstrip().startswith("#")
        for ln in src.splitlines()
    )
    if not has_router:
        print(f"❌ {fname}: APIRouter not used — add: router = APIRouter()")
        raise SystemExit(1)
print("✓ APIRouter used in both router files")

# ── include_router called ≥ 2 times ─────────────────────────────────────────

main_src = (mission / "task/main.py").read_text()
include_count = sum(
    1 for ln in main_src.splitlines()
    if "include_router" in ln and not ln.lstrip().startswith("#")
)
if include_count < 2:
    print(f"❌ task/main.py: app.include_router() called {include_count} time(s) — need ≥ 2")
    raise SystemExit(1)
print(f"✓ app.include_router() called {include_count} times in main.py")

# ── functional tests ──────────────────────────────────────────────────────────

try:
    from task.main import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import app from task.main: {exc}")
    raise SystemExit(1)

from fastapi.testclient import TestClient

client = TestClient(app)

r = client.get("/health")
if r.status_code != 200:
    print(f"❌ GET /health returned {r.status_code}")
    raise SystemExit(1)
print("✓ GET /health → 200")

r = client.get("/monsters")
if r.status_code != 200 or not r.json():
    print(f"❌ GET /monsters returned {r.status_code}: {r.text[:200]}")
    raise SystemExit(1)
print(f"✓ GET /monsters → 200, {len(r.json())} monsters")

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
print("✓ POST /battle/simulate → 200")

update_progress("04_api_routers")
print("\n✅ Mission 04 complete!")
