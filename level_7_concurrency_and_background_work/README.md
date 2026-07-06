# Level 7: Concurrency and Background Work

**Prerequisite:** Level 6 complete.

**Central thesis:** The API works — but long operations block it.
Learn to return a job_id immediately and execute work in the background.

## Starter: `starter_blocking_rpg_api/`

A working RPG tournament API where `POST /tournaments` blocks until simulation completes.

```bash
cd starter_blocking_rpg_api
uv run python cli.py simulate --battles 100
uv run pytest tests/ -q
```

## Missions

| # | Mission | Skill |
|---|---------|-------|
| 01 | [Blocking vs Background Work](missions/01_blocking_vs_background_work/README.md) | See the blocking problem |
| 02 | [asyncio Basics](missions/02_asyncio_basics/README.md) | async/await, gather, wait_for |
| 03 | [Async API Endpoints](missions/03_async_api_endpoints/README.md) | async def in FastAPI; I/O vs CPU |
| 04 | [Background Jobs](missions/04_background_jobs/README.md) | job_id pattern, threading.Thread |
| 05 | [Job Status Repository](missions/05_job_status_repository/README.md) | JobRepository Protocol |
| 06 | [Thread Pool for Blocking I/O](missions/06_thread_pool_for_blocking_io/README.md) | ThreadPoolExecutor |
| 07 | [Process Pool for CPU Work](missions/07_process_pool_for_cpu_work/README.md) | ProcessPoolExecutor |
| 08 | [Testing Background Work](missions/08_testing_background_work/README.md) | SyncWorker, deterministic tests |

## Projects

**Checkpoint:** [Project 01: Async Quest Aggregator](projects/01_async_quest_aggregator/README.md) — `asyncio.gather` with per-source timeout; partial results on failure.

**Checkpoint:** [Project 02: Background Report Queue](projects/02_background_report_queue/README.md) — `POST /reports` returns 202+job_id; `GET /reports/{id}` returns result when done.

**Boss Fight:** [Project 03: Concurrent Tournament Runner](projects/03_concurrent_tournament_runner/README.md) — background threading + ProcessPoolExecutor for CPU-bound battle simulation.

## How to start

Run from the repo root:

```bash
uv run python tools/course_status.py
```

To check a mission:

```bash
cd level_7_concurrency_and_background_work/missions/01_blocking_vs_background_work
uv run python check.py
```
