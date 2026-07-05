# Mission 07: Process Pool for CPU-Bound Work

## Goal

Use `ProcessPoolExecutor` to parallelize CPU-bound battle simulation across multiple processes.

## Given

- `_simulate_one(seed)` — simulates one battle deterministically from a seed (fully implemented)
- `simulate_tournament_sequential(n)` — runs `n` battles one by one (fully implemented)

## Your Task

Implement `simulate_tournament_parallel(n, workers=4)` using `ProcessPoolExecutor`.

```python
def simulate_tournament_parallel(n: int, workers: int = 4) -> dict:
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(_simulate_one, range(n)))
    hero_wins = sum(1 for r in results if r["winner"] == "hero")
    return {"total_battles": n, "hero_wins": hero_wins, "monster_wins": n - hero_wins}
```

Return the same dict format as `simulate_tournament_sequential`:
`{"total_battles": n, "hero_wins": int, "monster_wins": int}`

## Critical Requirement

`_simulate_one` **must stay module-level** (not a lambda or nested function). `ProcessPoolExecutor` pickles the worker function to send it to each worker process — only module-level functions are picklable.

## Hint

```python
pool.map(_simulate_one, range(n))
```

This maps the function over seeds 0, 1, 2, ..., n-1 in parallel.

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

All 3 checks must pass:
1. `simulate_tournament_sequential(2000)` returns correct counts
2. `simulate_tournament_parallel(2000, workers=4)` returns correct counts
3. `ProcessPoolExecutor` is used inside `simulate_tournament_parallel`

---

**Next:** [Mission 08 — Testing Background Work](../08_testing_background_work/README.md)
