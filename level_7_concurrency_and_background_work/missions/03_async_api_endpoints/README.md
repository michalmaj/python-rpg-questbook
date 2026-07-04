# Mission 03: Async API Endpoints

## Goal

Convert sync FastAPI endpoint handlers to `async def` and understand when it actually helps performance — and when it doesn't.

## Your task

Open `task/routers/tournaments.py` and change:

```python
def run_tournament(...)
```

to:

```python
async def run_tournament(...)
```

No other changes are needed. The function body stays the same.

## Key insight

`async def` only speeds things up for **I/O-bound work** — database queries, HTTP calls to external services, file reads. When Python awaits those operations, the event loop is free to handle other requests.

**CPU-bound work is different.** Battle simulation (`simulate_tournament`) runs pure Python math in a loop. There is nothing to `await`. Even with `async def`, the event loop stays blocked for the entire duration of the calculation. To parallelize CPU work, you need `ProcessPoolExecutor` (covered in a later mission).

The lesson: converting `def` → `async def` is the right default for FastAPI endpoints, but it is not a performance fix by itself.

## How to check

```bash
uv run python check.py
```

Run from the mission folder (`03_async_api_endpoints/`).
