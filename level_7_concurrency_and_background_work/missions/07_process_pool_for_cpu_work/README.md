# Mission 07: Process Pool for CPU-Bound Work

## Goal

Use `ProcessPoolExecutor` to parallelize CPU-bound battle simulation across multiple processes.

## Given

- `_simulate_one(seed)` — simulates one battle deterministically from a seed (fully implemented)
- `simulate_tournament_sequential(n)` — runs `n` battles one by one (fully implemented)

## Your Task

Implement `simulate_tournament_parallel(n, workers=4)` using `ProcessPoolExecutor`. Return
the same dict format as `simulate_tournament_sequential`:
`{"total_battles": n, "hero_wins": int, "monster_wins": int}`

**Requirements:**
- Distribute the `n` battles across the pool as independent work items — a single call that
  hands the whole tournament to one worker is not parallelism, it's one big task with extra
  steps.
- Each unit of work must actually run `_simulate_one` — don't reimplement the battle logic
  or substitute a different function.
- `ProcessPoolExecutor` supports both `pool.map(fn, iterable)` and multiple `pool.submit(fn, ...)`
  calls — either style is fine, including sending seeds in small chunks per call instead of
  one seed each.

### Syntax reminder

```python
with ProcessPoolExecutor(max_workers=workers) as pool:
    results = list(pool.map(_simulate_one, range(n)))  # one call per seed — or chunk it yourself
```

`results` is a list of `{"winner": ..., "rounds": ...}` dicts, one per seed — fold them into
the same `{"total_battles", "hero_wins", "monster_wins"}` shape `simulate_tournament_sequential`
already returns.

## Critical Requirement

`_simulate_one` **must stay module-level** (not a lambda or nested function). `ProcessPoolExecutor` pickles the worker function to send it to each worker process — only module-level functions are picklable.

## Hint

<details>
<summary>Full worked implementation (open only if you're stuck)</summary>

```python
def simulate_tournament_parallel(n: int, workers: int = 4) -> dict:
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(_simulate_one, range(n)))
    hero_wins = sum(1 for r in results if r["winner"] == "hero")
    return {"total_battles": n, "hero_wins": hero_wins, "monster_wins": n - hero_wins}
```

</details>

## Key Insight

Unlike `ThreadPoolExecutor`, `ProcessPoolExecutor` spawns separate OS processes. Each process has its own Python interpreter, so CPU-bound work **bypasses the GIL** and scales with CPU cores.

| Executor | GIL? | Good for |
|---|---|---|
| `ThreadPoolExecutor` | Yes (shared) | I/O-bound (network, disk) |
| `ProcessPoolExecutor` | No (separate) | CPU-bound (math, parsing) |

## Note on Overhead

For small `n`, parallel may be **slower** than sequential due to process startup and data serialization overhead. The benefit appears at larger `n` where computation outweighs setup cost.

## How to Check

```bash
uv run python check.py
```

All checks must pass:
1. `simulate_tournament_sequential(2000)` returns correct counts
2. `simulate_tournament_parallel(2000, workers=4)` returns the exact same `hero_wins` as the
   sequential run — `_simulate_one(seed)` is deterministic, so simulating the same seeds
   must land on the same result, not just "some number that adds up to 2000"
3. The pool actually distributes more than one independent work item — creating a pool and
   never calling `submit()`/`map()` on it (or handing it one task for the whole tournament)
   does not count as parallelizing
4. The worker function is picklable and a real `ProcessPoolExecutor` smoke test runs it
   across actual worker processes under your platform's start method

---

**Next:** [Mission 08 — Testing Background Work](../08_testing_background_work/README.md)
