# Mission 04: Background Jobs

## Goal

Implement the job-id pattern: `POST /tournaments → 202 + job_id`, `GET /jobs/{job_id} → status`.

## Your task

Open `task/routers/tournaments.py` and implement the two functions marked with `TODO`:

1. **`start_tournament`** — generate a `job_id`, store it in `_jobs`, start a background thread, return `JobStarted` with HTTP 202.
2. **`get_job`** — look up the job in `_jobs`, raise 404 if not found, return `JobOut` with all fields.

## Key insight

The endpoint returns immediately with a `job_id`. The actual tournament simulation runs in a background thread. The client polls `GET /jobs/{job_id}` to see when it finishes.

This is the **job-id pattern**: accept work → return a handle → let the client check back later.

## The smell

The global `_jobs` dict works for a single process, but it has problems:

- Not testable in isolation (shared state across requests)
- Not thread-safe for concurrent writes under load
- Lost on restart

Mission 05 fixes this with a proper `JobRepository`.

## How to check

Run from this folder:

```bash
uv run python check.py
```

A passing run looks like:

```
✓ POST /tournaments → 202, job_id=xxxxxxxx...
✓ GET /jobs/{job_id} → status=pending
✓ Job completed: {'total_battles': 20, ...}
✓ GET /jobs/unknown → 404
✓ POST /tournaments with battles=0 → 422

✅ Mission 04 complete! You built the job-id pattern.
```
