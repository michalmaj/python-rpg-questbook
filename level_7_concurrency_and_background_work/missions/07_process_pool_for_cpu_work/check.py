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
    except Exception as exc:
        print(f"❌ simulate_tournament_parallel({N}, workers=4) raised: {exc}")
        print("   Common cause: a lambda or closure was sent to the pool — not picklable.")
        raise SystemExit(1)

    if par["total_battles"] != N:
        print(f"❌ parallel: total_battles should be {N}, got {par['total_battles']}")
        raise SystemExit(1)
    if par["hero_wins"] + par["monster_wins"] != N:
        print("❌ parallel hero_wins + monster_wins must equal total_battles")
        raise SystemExit(1)
    # _simulate_one(seed) is fully deterministic given the seed, so a correct
    # parallel implementation simulating the same seeds 0..N-1 must land on
    # the exact same hero_wins as the sequential baseline — not just "some
    # number that adds up to N". Catches a worker that ignores its input and
    # returns a constant/fabricated result.
    if par["hero_wins"] != seq["hero_wins"]:
        print(f"❌ parallel hero_wins={par['hero_wins']} does not match sequential hero_wins={seq['hero_wins']}")
        print("   Both should simulate the same seeds 0..N-1 via _simulate_one and get identical counts.")
        print("   Common cause: the worker ignores its input seed, or doesn't call _simulate_one at all.")
        raise SystemExit(1)
    print(f"✓ simulate_tournament_parallel({N}, workers=4): {par_time:.3f}s, "
          f"hero_wins matches sequential baseline exactly")

    # ── Gate A: ProcessPoolExecutor must actually distribute multiple items ──
    #
    # A fake that creates the pool and never calls submit()/map() on it (or
    # submits the entire tournament as one opaque task) would still pass the
    # checks above. Replace ProcessPoolExecutor with a recording stand-in
    # that executes work inline (so results stay correct and no real
    # processes are needed here) but records every independent item handed
    # to submit()/map(). Gate B below proves the real thing works under
    # actual process + pickling semantics.
    import task as _task_mod

    class _RecordingFuture:
        def __init__(self, value=None, exc=None):
            self._value = value
            self._exc = exc

        def result(self, timeout=None):
            if self._exc is not None:
                raise self._exc
            return self._value

    class _RecordingProcessPoolExecutor:
        """Drop-in stand-in for ProcessPoolExecutor: runs work inline, records items."""

        instances: list = []

        def __init__(self, max_workers=None, *args, **kwargs):
            self.max_workers = max_workers
            self.submitted_items: list = []
            _RecordingProcessPoolExecutor.instances.append(self)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def submit(self, fn, *args, **kwargs):
            self.submitted_items.append((fn, args, kwargs))
            try:
                return _RecordingFuture(value=fn(*args, **kwargs))
            except Exception as exc:  # noqa: BLE001 - mirrors real Future semantics
                return _RecordingFuture(exc=exc)

        def map(self, fn, *iterables):
            results = []
            for call_args in zip(*iterables):
                self.submitted_items.append((fn, call_args, {}))
                results.append(fn(*call_args))
            return iter(results)

        def shutdown(self, wait=True, *args, **kwargs):
            pass

    N_SMALL = 8
    _RecordingProcessPoolExecutor.instances.clear()
    _original_executor = _task_mod.ProcessPoolExecutor
    _task_mod.ProcessPoolExecutor = _RecordingProcessPoolExecutor
    try:
        rec_result = simulate_tournament_parallel(N_SMALL, workers=4)
    finally:
        _task_mod.ProcessPoolExecutor = _original_executor

    total_items = sum(len(inst.submitted_items) for inst in _RecordingProcessPoolExecutor.instances)
    if total_items == 0:
        print("❌ ProcessPoolExecutor was created but never used (no submit()/map() calls).")
        print("   Creating the pool isn't enough — you must hand it the work.")
        raise SystemExit(1)
    if total_items < 2:
        print(f"❌ Only {total_items} independent work item was submitted to the pool.")
        print("   One opaque task for the whole tournament is not real distribution —")
        print("   each battle (or a chunk of battles) must be its own work item.")
        raise SystemExit(1)

    for fn, _args, _kwargs in (
        item for inst in _RecordingProcessPoolExecutor.instances for item in inst.submitted_items
    ):
        if getattr(fn, "__name__", "") == "<lambda>":
            print("❌ A lambda was submitted to the pool — ProcessPoolExecutor cannot pickle lambdas.")
            print("   Use the module-level _simulate_one function directly.")
            raise SystemExit(1)

    # If every item is a single plain seed (the expected pool.map(_simulate_one,
    # range(n)) shape), verify every seed 0..N_SMALL-1 was actually covered —
    # catches dropped/duplicated work under chunking-free implementations.
    _all_single_int = all(
        len(args) == 1 and isinstance(args[0], int) and not kwargs
        for inst in _RecordingProcessPoolExecutor.instances
        for _fn, args, kwargs in inst.submitted_items
    )
    if _all_single_int:
        _covered = {
            args[0]
            for inst in _RecordingProcessPoolExecutor.instances
            for _fn, args, _kwargs in inst.submitted_items
        }
        _missing = set(range(N_SMALL)) - _covered
        if _missing:
            print(f"❌ Not every seed was distributed to the pool — missing: {sorted(_missing)}")
            raise SystemExit(1)

    if not isinstance(rec_result, dict) or rec_result.get("total_battles") != N_SMALL:
        print(f"❌ simulate_tournament_parallel({N_SMALL}) returned wrong result: {rec_result}")
        raise SystemExit(1)
    print(f"✓ ProcessPoolExecutor actually used — {total_items} independent work items submitted, "
          f"result correct for {N_SMALL} battles")

    # ── Gate B: the real worker is picklable and runs under real spawn ───────
    import pickle
    from concurrent.futures import ProcessPoolExecutor as _RealProcessPoolExecutor

    _worker_fn = getattr(_task_mod, "_simulate_one", None)
    if _worker_fn is None:
        print("❌ task._simulate_one not found — required module-level worker function")
        raise SystemExit(1)
    try:
        pickle.dumps(_worker_fn)
    except Exception as exc:
        print(f"❌ _simulate_one is not picklable: {exc}")
        print("   Keep it as a top-level module function, never a lambda or nested def.")
        raise SystemExit(1)
    print("✓ _simulate_one is picklable (safe to send to worker processes)")

    with _RealProcessPoolExecutor(max_workers=2) as _smoke_pool:
        _smoke_results = list(_smoke_pool.map(_worker_fn, range(4)))
    if len(_smoke_results) != 4 or not all(isinstance(r, dict) and "winner" in r for r in _smoke_results):
        print(f"❌ ProcessPoolExecutor smoke test produced unexpected results: {_smoke_results}")
        raise SystemExit(1)
    print("✓ ProcessPoolExecutor smoke test: _simulate_one runs correctly across real worker processes (spawn-safe)")

    update_progress("07_process_pool_for_cpu_work")
    print("\n✅ Mission 07 complete! ProcessPoolExecutor for CPU-bound simulation.")
