# Mission 03: Async API Endpoints

## Goal

Understand when `async def` helps FastAPI endpoints — and when it actively makes things worse.

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

FastAPI treats `def` and `async def` very differently:

| Endpoint type | How FastAPI runs it | Good for |
|---|---|---|
| `def` | In a thread pool (non-blocking to the event loop) | Synchronous or CPU-bound code |
| `async def` | Directly on the event loop | True async I/O with `await` |

**`async def` helps when the body contains real `await` calls** — async database drivers, `httpx.AsyncClient`, `asyncio.sleep()`. The event loop can run other requests while waiting.

**`async def` hurts for CPU-bound work.** `simulate_tournament()` runs pure Python math with nothing to `await`. With `async def`, the event loop is blocked for the entire calculation — no other requests can be handled. With `def`, FastAPI runs it in a thread pool, keeping the event loop free.

This mission shows you what changing `def` → `async def` looks like. The *right* fix for CPU-bound endpoints is `ProcessPoolExecutor` (Mission 07) — not `async def`.

## Rule of thumb

```
async def  →  body has await calls (real async I/O)
def        →  synchronous code or CPU-bound work
processes  →  heavy CPU work that must not block the event loop
```

## How to check

```bash
uv run python check.py
```

Run from the mission folder (`03_async_api_endpoints/`).
