"""Check: Mission 01 — Blocking vs Background Work."""
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
    from task import time_tournament  # type: ignore[import]
except ImportError as exc:
    print(f"❌ Cannot import time_tournament from task.py: {exc}")
    raise SystemExit(1)

# scaffold check — exit early if student hasn't implemented the function yet
try:
    time_tournament(1)
except NotImplementedError:
    print("❌ time_tournament is not implemented yet — replace 'raise NotImplementedError' with your code")
    raise SystemExit(1)
except Exception:
    pass  # any real error = student modified it, continue to actual checks

# run the timing check
result = time_tournament(50)
for key in ("battles", "time_seconds", "battles_per_second"):
    if key not in result:
        print(f"❌ time_tournament result missing key '{key}'")
        raise SystemExit(1)
if result["battles"] != 50:
    print(f"❌ battles should be 50, got {result['battles']}")
    raise SystemExit(1)
if result["time_seconds"] < 0:
    print("❌ time_seconds must be non-negative")
    raise SystemExit(1)
print(f"✓ time_tournament(50) → {result['time_seconds']:.3f}s, "
      f"{result['battles_per_second']:.0f} battles/s")

# show the blocking problem with larger n
result_large = time_tournament(5000)
print(f"✓ time_tournament(5000) → {result_large['time_seconds']:.3f}s "
      f"(imagine 1_000_000 battles!)")

update_progress("01_blocking_vs_background_work")
print("\n✅ Mission 01 complete! You've seen the blocking problem.")
