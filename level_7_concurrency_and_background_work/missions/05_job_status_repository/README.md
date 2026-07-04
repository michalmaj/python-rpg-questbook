# Mission 05 — Job Status Repository

## Goal

Replace the global `_jobs` dict from M04 with a proper `JobRepository` Protocol. Learn how
dependency injection keeps business logic decoupled from storage details.

## What you are given (not a scaffold)

- **`task/jobs.py`** — full implementation of:
  - `JobRepository` Protocol
  - `InMemoryJobRepository` (thread-safe, stores jobs in memory)
  - `JsonJobRepository` (thread-safe, persists each job as a `.json` file)
- **`task/workers.py`** — full implementation of:
  - `BackgroundWorker` — submits jobs to a daemon thread (production use)
  - `SyncWorker` — runs jobs inline with no threading (for deterministic tests)

## Your task

Open **`task/routers/tournaments.py`** and implement the two functions:

1. **`start_tournament`** — create a job via `job_repo`, submit the simulation via `worker`,
   return `JobStarted` with the new `job_id`.

2. **`get_job`** — fetch the job from `job_repo`; raise `HTTPException(404)` if not found;
   otherwise return `JobOut`.

Both functions already receive `job_repo`, `worker`, and `svc` via FastAPI `Depends` — do not
reach for global state.

## Key insight

| Component | When to use |
|-----------|-------------|
| `InMemoryJobRepository` | Development and integration tests (fast, no I/O) |
| `JsonJobRepository` | When you need jobs to survive a server restart |
| `BackgroundWorker` | Production — runs simulation in a daemon thread |
| `SyncWorker` | Unit tests — deterministic, no `time.sleep` needed |

## How to check

```bash
uv run python check.py
```

Run from this mission's folder. The checker first validates `InMemoryJobRepository`,
`JsonJobRepository`, and `SyncWorker` directly (these pass immediately since `jobs.py` and
`workers.py` are provided). Then it hits the API — that part fails until you implement
`start_tournament` and `get_job`.
