# Mission 02: asyncio Basics

## Goal

Learn the three essential `asyncio` building blocks:
- **`async def` / `await`** — define and call asynchronous functions
- **`asyncio.gather`** — run multiple coroutines concurrently
- **`asyncio.wait_for`** — apply a hard timeout to any coroutine

These are the foundations for non-blocking I/O in Python.

## The Problem

Fetching monster data from a database or API takes time. If you fetch them one-by-one (sequentially), three monsters × 0.05s each = 0.15s total. But if you fetch them *simultaneously* (concurrently), all three can run in the time it takes one: ~0.05s total.

```
Sequential:  Fetch 1 (0.05s) → Fetch 2 (0.05s) → Fetch 3 (0.05s)  ≈ 0.15s total
Concurrent:  Fetch 1, 2, 3 all at once              ≈ 0.05s total
```

## Fake I/O: `asyncio.sleep()`

In this mission, we simulate slow database calls using `asyncio.sleep(0.05)`. This doesn't actually do I/O; it just pauses for 0.05 seconds and yields control to the event loop. The event loop can then run other tasks while waiting.

## Your Tasks

### 1. `fetch_monster_data(name: str) -> dict`

**What it does:**
- Simulates a slow database/API call
- Waits 0.05 seconds using `await asyncio.sleep(0.05)`
- Returns a dict: `{"name": name, "fetched": True}`

**Why it's async:**
- Any function that might block (network call, file I/O, database query) should be async
- The `await` inside lets other tasks run while we wait

### 2. `fetch_all_monsters(names: list[str]) -> list[dict]`

**What it does:**
- Fetches multiple monsters *concurrently* using `asyncio.gather`
- Instead of calling `fetch_monster_data` three times in a row (0.15s total), spawn all three tasks at once
- Wait for all to complete (0.05s total)

**Key insight:**
```python
# DON'T do this (sequential, slow):
results = []
for name in names:
    result = await fetch_monster_data(name)
    results.append(result)

# DO this (concurrent, fast):
results = await asyncio.gather(*[fetch_monster_data(n) for n in names])
```

The `asyncio.gather` unpacks a list of coroutines and runs them all at the same time.

### 3. `fetch_with_timeout(name: str, timeout: float) -> dict | None`

**What it does:**
- Fetches a monster, but with a time limit
- If the fetch completes within `timeout` seconds, return the result
- If it times out, catch `asyncio.TimeoutError` and return `None`

**How it works:**
```python
try:
    return await asyncio.wait_for(fetch_monster_data(name), timeout=timeout)
except asyncio.TimeoutError:
    return None
```

**Why it matters:**
- Real-world APIs sometimes hang or respond slowly
- Setting a timeout prevents your code from waiting forever

## How to Check

```bash
cd level_7_concurrency_and_background_work/missions/02_asyncio_basics
uv run python check.py
```

The check verifies:
1. `fetch_monster_data` returns the correct dict
2. `fetch_all_monsters` fetches 3 monsters in ~0.05s (proving concurrency)
3. `fetch_with_timeout` succeeds when timeout is generous (1.0s)
4. `fetch_with_timeout` returns `None` when timeout is tight (0.01s)

## Key Takeaways

- **Async functions don't run themselves.** You must `await` them or pass them to `asyncio.gather`, `asyncio.wait_for`, etc.
- **`asyncio.gather` = parallel execution.** It runs multiple coroutines at the same time (in the same thread, via the event loop).
- **`asyncio.wait_for` = timeout enforcement.** It's how you stop waiting after a deadline.
- **Timing is the proof.** If gather is working correctly, 3 fetches take ~0.05s, not 0.15s. The check.py verifies this.
