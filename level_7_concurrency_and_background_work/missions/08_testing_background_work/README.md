# Mission 08: Testing Background Work

## Goal

Write tests for the background job system using `SyncWorker`.

## Given

`task/` contains a complete working implementation:

- `InMemoryJobRepository` — stores jobs in memory with thread-safe access
- `BackgroundWorker` — submits jobs to a background thread (local single-process use)
- `SyncWorker` — runs jobs inline synchronously (for tests)
- `FastAPI` app with `/tournaments` and `/jobs/{job_id}` endpoints

## Your Task

Implement all 6 test functions in `task/tests/test_background.py`.

Each function currently raises `NotImplementedError` — replace the body with a real test.

## Key Rules

**Use `SyncWorker`, not `BackgroundWorker`.**  
`SyncWorker` runs jobs inline — no threads, no timing issues. Your tests are deterministic.

**No `time.sleep()`.**  
If you find yourself reaching for `sleep()`, your test is non-deterministic. Use `SyncWorker` instead.

## Pattern

Create fresh instances per test — do not share state between tests:

```python
repo = InMemoryJobRepository()
worker = SyncWorker(repo)
```

## Test Functions to Implement

| Function | What to test |
|---|---|
| `test_new_job_is_pending` | A new job starts with status `"pending"` |
| `test_job_completes_after_submit` | After `worker.submit()`, status is `"completed"` |
| `test_failed_job_stores_error` | If the job function raises, status is `"failed"` and error is stored |
| `test_job_result_stored` | Job result dict is stored correctly after completion |
| `test_two_jobs_are_independent` | Two jobs don't overwrite each other's results |
| `test_unknown_job_returns_none` | `repo.get("nonexistent")` returns `None` |

## How to Check

```bash
uv run python check.py
```

Run from the mission folder. All 6 tests must pass.
