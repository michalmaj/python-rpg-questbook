"""check.py — Project 01: Battle Preview API"""

import ast
import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[3] / "level_6_api" / ".progress"
TASK_FILE = PROJECT_DIR / "task.py"

sys.path.insert(0, str(PROJECT_DIR))


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


def main() -> None:
    # ── 1. Import app ─────────────────────────────────────────────────────────
    try:
        from fastapi.testclient import TestClient
        from task import app
    except ImportError as exc:
        print(f"❌ Cannot import: {exc}")
        print("   Install: uv add fastapi httpx")
        raise SystemExit(1)

    client = TestClient(app, raise_server_exceptions=False)

    # ── 2. Scaffold guard ─────────────────────────────────────────────────────
    r = client.get("/health")
    if r.status_code == 500 and "NotImplementedError" in r.text:
        print("❌ task.py is not implemented yet — replace NotImplementedError with real code")
        raise SystemExit(1)

    # ── 3. GET /health → 200 ─────────────────────────────────────────────────
    r = client.get("/health")
    if r.status_code != 200:
        print(f"❌ GET /health → {r.status_code}, expected 200")
        raise SystemExit(1)
    print("✓ GET /health → 200")

    # ── 4. POST /heroes/preview valid → 200 + power_rating ───────────────────
    payload = {"name": "Ada", "hp": 120, "atk": 15, "def_": 5}
    r = client.post("/heroes/preview", json=payload)
    if r.status_code != 200:
        print(f"❌ POST /heroes/preview → {r.status_code}, expected 200")
        print(r.text)
        raise SystemExit(1)
    body = r.json()
    if "power_rating" not in body:
        print(f"❌ Response missing 'power_rating': {body}")
        raise SystemExit(1)
    expected_pr = round(15 / (5 + 1), 2)
    if abs(body["power_rating"] - expected_pr) > 0.01:
        print(f"❌ power_rating should be {expected_pr}, got {body['power_rating']}")
        raise SystemExit(1)
    print(f"✓ POST /heroes/preview → 200, power_rating={body['power_rating']}")

    # ── 5. POST /heroes/preview invalid (hp=-1) → 422 ────────────────────────
    r = client.post("/heroes/preview", json={"name": "X", "hp": -1, "atk": 5, "def_": 0})
    if r.status_code != 422:
        print(f"❌ POST /heroes/preview hp=-1 → {r.status_code}, expected 422")
        raise SystemExit(1)
    print("✓ POST /heroes/preview with hp=-1 → 422 (Pydantic validation)")

    # ── 6. POST /battle/simulate valid → 200 + winner + rounds + hero_hp_remaining
    payload = {"hero": {"name": "Ada", "hp": 120, "atk": 15, "def_": 5},
               "monster_name": "Goblin"}
    r = client.post("/battle/simulate", json=payload)
    if r.status_code != 200:
        print(f"❌ POST /battle/simulate → {r.status_code}, expected 200")
        print(r.text)
        raise SystemExit(1)
    body = r.json()
    for field in ("winner", "rounds", "hero_hp_remaining"):
        if field not in body:
            print(f"❌ Response missing '{field}': {body}")
            raise SystemExit(1)
    if body["winner"] not in ("hero", "monster"):
        print(f"❌ winner must be 'hero' or 'monster', got {body['winner']!r}")
        raise SystemExit(1)
    print(f"✓ POST /battle/simulate → 200, winner={body['winner']!r}, rounds={body['rounds']}")

    # ── 7. POST /battle/simulate unknown monster → 404 ───────────────────────
    payload = {"hero": {"name": "Ada", "hp": 120, "atk": 15, "def_": 5},
               "monster_name": "Phoenix"}
    r = client.post("/battle/simulate", json=payload)
    if r.status_code != 404:
        print(f"❌ Unknown monster should return 404, got {r.status_code}")
        raise SystemExit(1)
    print("✓ POST /battle/simulate unknown monster → 404")

    # ── 8. AST check: no APIRouter ────────────────────────────────────────────
    source = TASK_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    uses_router = any(
        isinstance(node, ast.Name) and node.id == "APIRouter"
        for node in ast.walk(tree)
    )
    if uses_router:
        print("❌ task.py must NOT use APIRouter (that's Project 02 — keep this one simple)")
        raise SystemExit(1)
    print("✓ No APIRouter used (single-file checkpoint constraint)")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("01_battle_preview_api")
    print()
    print("✅ Project 01 complete: Battle Preview API works!")
    print()
    print("   Three endpoints, Pydantic schemas, HTTPException(404).")
    print("   FastAPI + Pydantic handle validation automatically — you just declare the types.")


if __name__ == "__main__":
    main()
