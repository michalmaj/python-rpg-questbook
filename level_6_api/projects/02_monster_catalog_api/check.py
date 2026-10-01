"""check.py — Project 02: Monster Catalog API"""

import ast
import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[3] / "level_6_api" / ".progress"
ROUTER_FILE = PROJECT_DIR / "task" / "routers" / "monsters.py"
REPO_FILE = PROJECT_DIR / "task" / "repository.py"

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


def _uses_name(source: str, name: str) -> bool:
    tree = ast.parse(source)
    return any(
        (isinstance(n, ast.Name) and n.id == name) or
        (isinstance(n, ast.Attribute) and n.attr == name)
        for n in ast.walk(tree)
    )


def _has_module_level_dict(source: str) -> bool:
    """Return True if there is a module-level dict assignment (global state smell)."""
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Dict):
                return True
    return False


def main() -> None:
    # ── 1. Import app ─────────────────────────────────────────────────────────
    try:
        from fastapi.testclient import TestClient
        from task.main import app
    except ImportError as exc:
        print(f"❌ Cannot import: {exc}")
        print("   Install: uv add fastapi httpx")
        raise SystemExit(1)

    client = TestClient(app, raise_server_exceptions=False)

    # ── 2. Scaffold guard ─────────────────────────────────────────────────────
    r = client.get("/monsters")
    if r.status_code == 500 and "NotImplementedError" in r.text:
        print("❌ task/ is not implemented yet — replace NotImplementedError with real code")
        raise SystemExit(1)

    # ── 3. GET /monsters → 200, matches the real provided catalog ───────────
    # Not just "≥2 items" — a hardcoded fake list would pass a length-only
    # check. The catalog is fixed/provided (task/repository.py's _CATALOG),
    # so compare the actual response against it field-by-field, as a set
    # (the API contract doesn't guarantee ordering).
    r = client.get("/monsters")
    if r.status_code != 200:
        print(f"❌ GET /monsters → {r.status_code}, expected 200")
        print(r.text)
        raise SystemExit(1)
    monsters = r.json()
    if not isinstance(monsters, list) or len(monsters) < 2:
        print(f"❌ GET /monsters must return list with ≥2 monsters, got {monsters}")
        raise SystemExit(1)

    from task.repository import _CATALOG  # type: ignore[import]

    expected = {
        (entry["name"], entry["hp"], entry["atk"], entry["def_"])
        for entry in _CATALOG
    }
    actual = {
        (m.get("name"), m.get("hp"), m.get("atk"), m.get("def_"))
        for m in monsters
    }
    if actual != expected:
        print(f"❌ GET /monsters returned {sorted(actual)}, "
              f"but the real catalog has {sorted(expected)}")
        print("   Return the real monsters from the repository, not hardcoded/fake data.")
        raise SystemExit(1)
    print(f"✓ GET /monsters → 200, {len(monsters)} monsters matching the real catalog")

    # ── 4. GET /monsters/Goblin → 200 ────────────────────────────────────────
    r = client.get("/monsters/Goblin")
    if r.status_code != 200:
        print(f"❌ GET /monsters/Goblin → {r.status_code}, expected 200")
        print(r.text)
        raise SystemExit(1)
    body = r.json()
    if body.get("name", "").lower() != "goblin":
        print(f"❌ GET /monsters/Goblin returned wrong monster: {body}")
        raise SystemExit(1)
    print("✓ GET /monsters/Goblin → 200")

    # ── 5. GET /monsters/Unknown → 404 ───────────────────────────────────────
    r = client.get("/monsters/Unknown")
    if r.status_code != 404:
        print(f"❌ GET /monsters/Unknown → {r.status_code}, expected 404")
        raise SystemExit(1)
    print("✓ GET /monsters/Unknown → 404")

    # ── 6. GET /monsters/Goblin/difficulty → easy ────────────────────────────
    r = client.get("/monsters/Goblin/difficulty")
    if r.status_code != 200:
        print(f"❌ GET /monsters/Goblin/difficulty → {r.status_code}, expected 200")
        print(r.text)
        raise SystemExit(1)
    body = r.json()
    if body.get("difficulty") != "easy":
        print(f"❌ Goblin (30 HP) should be 'easy', got {body.get('difficulty')!r}")
        raise SystemExit(1)
    print("✓ GET /monsters/Goblin/difficulty → easy")

    # ── 7. GET /monsters/Dragon/difficulty → hard ────────────────────────────
    r = client.get("/monsters/Dragon/difficulty")
    if r.status_code != 200:
        print(f"❌ GET /monsters/Dragon/difficulty → {r.status_code}, expected 200")
        print(r.text)
        raise SystemExit(1)
    body = r.json()
    if body.get("difficulty") != "hard":
        print(f"❌ Dragon (200 HP) should be 'hard', got {body.get('difficulty')!r}")
        raise SystemExit(1)
    print("✓ GET /monsters/Dragon/difficulty → hard")

    # ── 8. AST: APIRouter used in routers/monsters.py ────────────────────────
    router_source = ROUTER_FILE.read_text(encoding="utf-8")
    if not _uses_name(router_source, "APIRouter"):
        print("❌ routers/monsters.py must use APIRouter")
        raise SystemExit(1)
    print("✓ APIRouter used in routers/monsters.py")

    # ── 9. AST: Depends used in router ───────────────────────────────────────
    if not _uses_name(router_source, "Depends"):
        print("❌ routers/monsters.py must use Depends() for dependency injection")
        raise SystemExit(1)
    print("✓ Depends() used in routers/monsters.py")

    # ── 10. AST: no module-level dict in router (no global state) ────────────
    if _has_module_level_dict(router_source):
        print("❌ routers/monsters.py must NOT have a module-level dict")
        print("   Use Depends(get_monster_repo) instead of a global variable")
        raise SystemExit(1)
    print("✓ No module-level dict in router (clean DI)")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("02_monster_catalog_api")
    print()
    print("✅ Project 02 complete: Monster Catalog API works!")
    print()
    print("   APIRouter + Depends + HTTPException(404) — the FastAPI trio.")
    print("   The router has no global state; the dependency provides it.")


if __name__ == "__main__":
    main()
