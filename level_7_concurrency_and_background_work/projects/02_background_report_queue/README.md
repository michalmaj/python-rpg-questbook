# Project 02: Background Report Queue

**Level 7 — Concurrency and Background Work**

## Goal

The Guild Master wants a report on the last 5 combat sessions: win rates, average damage, a Markdown summary. Generating the report is slow enough that the API should return immediately with a job ID and process it in the background.

You will implement `BackgroundWorker` — the piece that runs the computation in a daemon thread so the HTTP request doesn't block.

## Your task

Open `task/jobs.py` and implement `BackgroundWorker.submit`.

```python
class BackgroundWorker:
    def __init__(self, repo: InMemoryJobRepository) -> None:
        self._repo = repo            # already implemented for you

    def submit(self, job_id: str, fn: Callable[[], Any]) -> None:
        # your implementation here
        ...
```

**Requirements:**

1. Set job status to `"running"` immediately
2. Start a **daemon** thread that calls `fn()`
3. On success: call `self._repo.set_result(job_id, result)` (sets status to `"completed"`)
4. On exception: call `self._repo.set_error(job_id, str(exc))` (sets status to `"failed"`)
5. `submit()` must return **before** `fn()` finishes — that is the whole point

Do **not** modify `InMemoryJobRepository`, `SyncWorker`, or any file outside `task/jobs.py`.

## Project structure

```
task/
├── main.py           # FastAPI app (do not modify)
├── routers/
│   └── reports.py    # POST /reports, GET /reports/{job_id} (do not modify)
├── dependencies.py   # DI wiring (do not modify)
├── schemas.py        # Pydantic models (do not modify)
├── report.py         # compute_report() — reads session JSON files (do not modify)
├── jobs.py           # ← EDIT THIS FILE
└── data/
    └── sessions/
        ├── session_001.json  # Aragorn hero_win
        ├── session_002.json  # Legolas monster_win
        ├── session_003.json  # Gimli hero_win
        ├── session_004.json  # Frodo hero_win
        └── session_005.json  # Gandalf monster_win
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check |
| POST | `/reports` | Enqueue a report job → `{"job_id": "..."}` (202) |
| GET | `/reports/{job_id}` | Poll job status and result |

## Run the checker

```bash
uv run python check.py
```

All gates must pass:

| Gate | What it checks |
|------|---------------|
| 1 | App imports without error |
| 2 | Scaffold guard — `submit` must be implemented |
| 3 | `GET /health` → 200 |
| 4 | `POST /reports` → 202 with `job_id` |
| 5 | `GET /reports/{id}` → completed with `total_sessions`, `hero_win_rate`, `markdown` |
| 6 | `hero_win_rate` = 0.6 (3 wins / 5 sessions) |
| 7 | Unknown `job_id` → 404 |
| 8 | Malformed JSON body → 422 |
| 9 | `BackgroundWorker` + `SyncWorker` both in `jobs.py` (AST) |
| 10 | `BackgroundWorker` uses `threading.Thread` (AST) |

## Hint

<details>
<summary>Structure hint</summary>

```python
def submit(self, job_id: str, fn: Callable[[], Any]) -> None:
    self._repo.set_status(job_id, "running")
    thread = threading.Thread(target=self._run, args=(job_id, fn), daemon=True)
    thread.start()

def _run(self, job_id: str, fn: Callable[[], Any]) -> None:
    try:
        result = fn()
        self._repo.set_result(job_id, result)
    except Exception as exc:
        self._repo.set_error(job_id, str(exc))
```

</details>

## Concepts practised

- `threading.Thread(daemon=True)` — background thread that doesn't block process exit
- Job queue pattern: create → submit → poll
- `dependency_overrides` — swapping `BackgroundWorker` for `SyncWorker` in tests
- Fire-and-forget + status tracking via shared repository
