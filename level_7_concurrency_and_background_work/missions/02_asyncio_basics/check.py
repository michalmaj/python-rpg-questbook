"""Check: Mission 02 — asyncio Basics."""
import asyncio
import json
import sys
import time
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
    from task import fetch_all_monsters, fetch_monster_data, fetch_with_timeout  # type: ignore
except ImportError as exc:
    print(f"❌ Cannot import functions from task.py: {exc}")
    raise SystemExit(1)

# ── fetch_monster_data ────────────────────────────────────────────────────────
result = asyncio.run(fetch_monster_data("Goblin"))
if not isinstance(result, dict) or result.get("name") != "Goblin":
    print(f"❌ fetch_monster_data('Goblin') should return dict with name='Goblin', got {result}")
    raise SystemExit(1)
print("✓ fetch_monster_data('Goblin') → correct dict")

# ── fetch_all_monsters — must use gather (concurrent) ─────────────────────────
names = ["Goblin", "Orc", "Dragon"]
t0 = time.perf_counter()
results = asyncio.run(fetch_all_monsters(names))
elapsed = time.perf_counter() - t0
if len(results) != 3:
    print(f"❌ fetch_all_monsters should return 3 items, got {len(results)}")
    raise SystemExit(1)
if elapsed > 0.12:
    print(f"❌ fetch_all_monsters({names}) took {elapsed:.3f}s — should be ~0.05s (use asyncio.gather)")
    raise SystemExit(1)
print(f"✓ fetch_all_monsters(3 monsters) → {elapsed:.3f}s (concurrent, not sequential)")

# ── fetch_with_timeout — success ──────────────────────────────────────────────
result = asyncio.run(fetch_with_timeout("Goblin", timeout=1.0))
if result is None:
    print("❌ fetch_with_timeout('Goblin', 1.0) timed out unexpectedly")
    raise SystemExit(1)
print("✓ fetch_with_timeout('Goblin', 1.0) → success")

# ── fetch_with_timeout — actual timeout ───────────────────────────────────────
result = asyncio.run(fetch_with_timeout("Goblin", timeout=0.01))
if result is not None:
    print("❌ fetch_with_timeout with 0.01s timeout should return None")
    raise SystemExit(1)
print("✓ fetch_with_timeout('Goblin', 0.01) → None (timeout)")

update_progress("02_asyncio_basics")
print("\n✅ Mission 02 complete! You know async/await, gather, and timeouts.")
