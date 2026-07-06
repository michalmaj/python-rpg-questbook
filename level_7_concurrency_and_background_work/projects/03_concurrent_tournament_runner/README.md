# Boss Fight: Concurrent Tournament Runner

## Goal

Build a non-blocking tournament API with background job tracking. Instead of blocking the client while battles run, the API immediately returns a `job_id` and processes the work in a background thread. Clients poll for status and retrieve the Markdown report when the job completes.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/tournaments` | Start a background tournament → `202 Accepted` + `job_id` |
| `GET` | `/tournaments/{job_id}` | Poll job status and result |
| `GET` | `/tournaments/{job_id}/report` | Retrieve Markdown report (only when completed) |

## Your Task

Implement all three endpoints in `api/routers/tournaments.py`. Each endpoint currently raises `NotImplementedError` — replace with the real logic.

Then write at least **6 tests** in `tests/test_api.py` covering:
1. `POST /tournaments` → 202 + `job_id`
2. `GET /tournaments/{job_id}` → `completed` status with `result`
3. `GET /tournaments/{job_id}/report` → Markdown `text/plain`
4. `GET /tournaments/nonexistent` → 404
5. `POST /tournaments` with `battles=0` → 422
6. `GET /tournaments/{job_id}/report` when not completed → 425

## Key Rules

- Use `SyncWorker` in tests via `app.dependency_overrides` for determinism (never `BackgroundWorker` in tests)
- No `time.sleep()` in tests
- `SyncWorker` runs the job inline before returning, so the job is always `completed` when you poll immediately after `POST`

## How to Check

```bash
uv run python check.py
```

All 9 gates must pass.
