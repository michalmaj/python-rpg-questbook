# level_6_api/missions/08_openapi_and_api_polish/check.py
"""Check: Mission 08 — OpenAPI and API Polish."""
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
    from task.main import app  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import app from task.main: {exc}")
    raise SystemExit(1)

from fastapi.testclient import TestClient

client = TestClient(app)

# ── FastAPI() has title, description, version ─────────────────────────────────

main_src = (Path(__file__).parent / "task/main.py").read_text()
for attr in ("title=", "description=", "version="):
    if attr not in main_src:
        print(f"❌ FastAPI() missing {attr} — add it to app = FastAPI(...)")
        raise SystemExit(1)
print("✓ FastAPI() has title, description, version")

# ── tags used on include_router ───────────────────────────────────────────────

tags_count = sum(
    1 for ln in main_src.splitlines()
    if "tags=" in ln and "include_router" in ln and not ln.lstrip().startswith("#")
)
if tags_count < 2:
    print(f"❌ tags= on include_router() found {tags_count} times — need ≥ 2 routers with tags")
    raise SystemExit(1)
print(f"✓ tags= used on {tags_count} routers")

# ── OpenAPI schema has tags ────────────────────────────────────────────────────

r = client.get("/openapi.json")
if r.status_code != 200:
    print(f"❌ GET /openapi.json returned {r.status_code}")
    raise SystemExit(1)
schema = r.json()
tags_in_schema = {tag["name"] for tag in schema.get("tags", [])}
if not tags_in_schema:
    paths = schema.get("paths", {})
    tags_from_paths: set[str] = set()
    for path_item in paths.values():
        for op in path_item.values():
            if isinstance(op, dict):
                tags_from_paths.update(op.get("tags", []))
    if not tags_from_paths:
        print("❌ No tags found in OpenAPI schema — add tags= to include_router()")
        raise SystemExit(1)
print("✓ OpenAPI schema contains tags")

# ── GET /openapi.json has description ────────────────────────────────────────

if not schema.get("info", {}).get("description"):
    print("❌ OpenAPI info.description is empty — add description= to FastAPI()")
    raise SystemExit(1)
print("✓ OpenAPI info has description")

update_progress("08_openapi_and_api_polish")
print("\n✅ Mission 08 complete!")
