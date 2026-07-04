"""Check: Mission 07 — Process Pool for CPU-Bound Work."""
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
    from task import simulate_tournament_parallel, simulate_tournament_sequential  # type: ignore
except ImportError as exc:
    print(f"❌ Cannot import from task.py: {exc}")
    raise SystemExit(1)

if __name__ == "__main__":
    N = 2000

    # sequential baseline
    t0 = time.perf_counter()
    seq = simulate_tournament_sequential(N)
    seq_time = time.perf_counter() - t0
    if seq["total_battles"] != N:
        print(f"❌ sequential: total_battles should be {N}, got {seq['total_battles']}")
        raise SystemExit(1)
    if seq["hero_wins"] + seq["monster_wins"] != N:
        print("❌ hero_wins + monster_wins must equal total_battles")
        raise SystemExit(1)
    print(f"✓ simulate_tournament_sequential({N}): {seq_time:.3f}s")

    # parallel
    try:
        t0 = time.perf_counter()
        par = simulate_tournament_parallel(N, workers=4)
        par_time = time.perf_counter() - t0
    except NotImplementedError:
        print("❌ simulate_tournament_parallel not implemented")
        raise SystemExit(1)

    if par["total_battles"] != N:
        print(f"❌ parallel: total_battles should be {N}, got {par['total_battles']}")
        raise SystemExit(1)
    if par["hero_wins"] + par["monster_wins"] != N:
        print("❌ parallel hero_wins + monster_wins must equal total_battles")
        raise SystemExit(1)
    print(f"✓ simulate_tournament_parallel({N}, workers=4): {par_time:.3f}s")

    # verify ProcessPoolExecutor used
    src = (Path(__file__).parent / "task.py").read_text()
    if "ProcessPoolExecutor" not in src:
        print("❌ task.py must use ProcessPoolExecutor")
        raise SystemExit(1)
    print("✓ ProcessPoolExecutor used in task.py")

    update_progress("07_process_pool_for_cpu_work")
    print("\n✅ Mission 07 complete! ProcessPoolExecutor for CPU-bound simulation.")
