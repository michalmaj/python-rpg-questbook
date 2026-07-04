"""Check: Mission 03 — Async API Endpoints."""
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

import warnings
warnings.filterwarnings("ignore")

from fastapi.testclient import TestClient

client = TestClient(app)

# ── async def used on /tournaments ────────────────────────────────────────────
src = (Path(__file__).parent / "task" / "routers" / "tournaments.py").read_text()
code_lines = [ln for ln in src.splitlines() if not ln.lstrip().startswith("#")]
code_src = "\n".join(code_lines)
if "async def run_tournament" not in code_src:
    print("❌ run_tournament must be 'async def' — convert from sync")
    raise SystemExit(1)
print("✓ run_tournament is async def")

# ── async def on health ───────────────────────────────────────────────────────
main_src = (Path(__file__).parent / "task" / "main.py").read_text()
if "async def health" not in main_src:
    print("❌ health endpoint should be async def")
    raise SystemExit(1)
print("✓ health endpoint is async def")

# ── /tournaments still works ──────────────────────────────────────────────────
r = client.post("/tournaments", json={"battles": 10})
if r.status_code != 200:
    print(f"❌ POST /tournaments returned {r.status_code}: {r.text[:200]}")
    raise SystemExit(1)
data = r.json()
if data.get("total_battles") != 10:
    print(f"❌ total_battles should be 10, got {data.get('total_battles')}")
    raise SystemExit(1)
print("✓ POST /tournaments → 200, total_battles=10")

update_progress("03_async_api_endpoints")
print("\n✅ Mission 03 complete! async def endpoints — remember: async ≠ faster for CPU work.")
