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

# ProcessPoolExecutor (macOS "spawn" start method) re-imports this script in worker
# processes. Without this guard, each worker would re-run all the checks, causing
# BrokenProcessPool errors. The import above must stay at module level to catch
# missing functions early; all check logic lives inside the guard.
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

    # verify ProcessPoolExecutor is actually used inside simulate_tournament_parallel
    import ast

    src = (Path(__file__).parent / "task.py").read_text()
    tree = ast.parse(src)
    parallel_func = next(
        (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "simulate_tournament_parallel"),
        None,
    )
    if parallel_func is None:
        print("❌ simulate_tournament_parallel not found in task.py")
        raise SystemExit(1)

    func_src = ast.get_source_segment(src, parallel_func) or ""
    if "ProcessPoolExecutor" not in func_src:
        print("❌ simulate_tournament_parallel must use ProcessPoolExecutor (found import but not used in the function body)")
        raise SystemExit(1)
    print("✓ ProcessPoolExecutor used inside simulate_tournament_parallel")

    update_progress("07_process_pool_for_cpu_work")
    print("\n✅ Mission 07 complete! ProcessPoolExecutor for CPU-bound simulation.")
