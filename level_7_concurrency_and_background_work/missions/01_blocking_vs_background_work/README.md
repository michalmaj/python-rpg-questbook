# Mission 01: Blocking vs Background Work

## Goal

Understand why `simulate_tournament()` is a **blocking** operation — it occupies the calling
thread completely until every battle has finished. In a web API this means no other request
can be served while the tournament runs.

## Your task

Open `task.py` and implement `time_tournament(n: int) -> dict`.

The function must:
1. Call `_svc.simulate_tournament(n)` to run `n` battles.
2. Measure how long the call takes (wall-clock time).
3. Return a dict with exactly these keys:

```python
{
    "battles": n,                # int — number of battles simulated
    "time_seconds": float,       # wall-clock seconds the call took
    "battles_per_second": float, # throughput: n / time_seconds
}
```

## How to check

```bash
uv run python check.py
```

Run this from inside the mission folder. The checker will:
- Confirm the scaffold raises `NotImplementedError` (so you know you have not already solved it).
- Call `time_tournament(50)` and verify all three keys are present and correct.
- Call `time_tournament(5000)` so you can see how the time scales.

## Key insight

Notice how the time grows roughly linearly with `n`. Double the battles → double the wait.
In a FastAPI route that calls `simulate_tournament(100_000)`, **every HTTP request that
arrives while the tournament runs must wait in queue** — the event loop is blocked.

That is the problem Level 7 teaches you to fix: move heavy work off the main thread so
the API stays responsive.

---

**Next:** [Mission 02 — asyncio Basics](../02_asyncio_basics/README.md)
