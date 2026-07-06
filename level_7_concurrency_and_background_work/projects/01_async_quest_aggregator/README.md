# Project 01: Async Quest Aggregator

**Level 7 — Concurrency and Background Work**

## Goal

The Guild Hall board shows quests from three sources: the Adventurers' Guild, the Village Elder, and the Royal Court. Each source has its own network latency. A busy royal courier shouldn't make every hero wait.

Implement `aggregate_all_quests(timeout)` so all three sources are fetched **concurrently**, and any source that exceeds the per-source timeout is skipped gracefully — its quests simply don't appear this round.

## Your task

Open `task.py` and implement `aggregate_all_quests`.

```python
async def aggregate_all_quests(timeout: float) -> AggregateResult:
    ...
```

**Requirements:**

- Use `asyncio.gather(..., return_exceptions=True)` to fire all three fetches at once
- Wrap each source coroutine with `asyncio.wait_for(..., timeout=timeout)` for a per-source timeout
- Sources that raise `TimeoutError` (or any other exception) → their name goes into `failed_sources`
- Successfully fetched quests → merged into `quests` list
- Record wall-clock elapsed time using `time.monotonic`

The three pre-built source functions (`fetch_guild_quests`, `fetch_village_quests`, `fetch_royal_quests`) and the `SOURCES` dict are already wired up — do not modify them.

## Run the checker

```bash
uv run python check.py
```

All 5 gates must pass:

| Gate | What it checks |
|------|---------------|
| 1 | `AggregateResult` has `quests`, `failed_sources`, `elapsed` |
| 2 | `timeout=5.0` → all 3 sources succeed, ≥ 3 quests |
| 3 | `timeout=0.15` → royal (0.2s) fails, guild (0.1s) and village (0.05s) succeed |
| 4 | Wall-clock for full run < 0.4s (concurrent, not sequential) |
| 5 | `asyncio.gather()` present inside `aggregate_all_quests` (AST check) |

## Hints

<details>
<summary>Structure hint</summary>

```python
async def aggregate_all_quests(timeout: float) -> AggregateResult:
    t0 = time.monotonic()
    tasks = [
        asyncio.wait_for(fn(), timeout=timeout)
        for fn in SOURCES.values()
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    quests: list[Quest] = []
    failed: list[str] = []
    for name, result in zip(SOURCES.keys(), results):
        if isinstance(result, Exception):
            failed.append(name)
        else:
            quests.extend(result)
    return AggregateResult(quests=quests, failed_sources=failed, elapsed=time.monotonic() - t0)
```

</details>

## Concepts practised

- `asyncio.gather` — run multiple coroutines concurrently
- `asyncio.wait_for` — per-coroutine timeout
- `return_exceptions=True` — gather doesn't raise; exceptions arrive as values
- Wall-clock timing with `time.monotonic`

---

**Next:** `level_7_concurrency_and_background_work/projects/02_background_report_queue/README.md`
