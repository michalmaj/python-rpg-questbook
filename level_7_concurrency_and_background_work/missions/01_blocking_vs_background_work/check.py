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
    import task as _task_mod
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

# ── behavioral spy: time_tournament must actually call _svc.simulate_tournament ──
#
# A fake that just does `return {"battles": n, "time_seconds": 0.0, ...}`
# without ever touching the service would still satisfy a shape-only check.
# Wrap the real simulate_tournament with a spy that records how it was
# called, but still delegates to the real implementation — so the timing
# and result stay genuine.
if not hasattr(_task_mod, "_svc"):
    print("❌ task.py: expected module-level _svc (SimulationService) not found")
    raise SystemExit(1)

_spy_calls: list[int] = []
_original_simulate = _task_mod._svc.simulate_tournament


def _spy_simulate(n: int):
    _spy_calls.append(n)
    return _original_simulate(n)


_task_mod._svc.simulate_tournament = _spy_simulate
try:
    _spy_calls.clear()
    SPY_N = 7
    spy_result = time_tournament(SPY_N)
    if not _spy_calls:
        print(f"❌ time_tournament({SPY_N}) never called _svc.simulate_tournament()")
        print("   You can't measure a blocking call you don't actually make.")
        raise SystemExit(1)
    if SPY_N not in _spy_calls:
        print(f"❌ time_tournament({SPY_N}) called simulate_tournament with {_spy_calls}, "
              f"expected it to pass battles={SPY_N} through")
        raise SystemExit(1)
    if spy_result.get("battles") != SPY_N:
        print(f"❌ time_tournament({SPY_N}) returned battles={spy_result.get('battles')!r}, expected {SPY_N}")
        raise SystemExit(1)
finally:
    _task_mod._svc.simulate_tournament = _original_simulate
print(f"✓ time_tournament() actually calls _svc.simulate_tournament(battles) — not hardcoded")

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
