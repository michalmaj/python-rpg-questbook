"""Mission 08: Testing Background Work.

Write tests for the background job system. Use SyncWorker — it runs jobs
inline so tests are deterministic (no race conditions, no sleep()).

Rules:
  - Import SyncWorker from task.workers
  - Import InMemoryJobRepository from task.jobs
  - Do NOT use sleep() or threading.Event in these tests
"""
import pytest
from task.jobs import InMemoryJobRepository, JobStatus
from task.workers import SyncWorker


# ── TODO 1 ───────────────────────────────────────────────────────────────────
# Test that a new job starts as "pending" after create().
def test_new_job_is_pending() -> None:
    raise NotImplementedError


# ── TODO 2 ───────────────────────────────────────────────────────────────────
# Test that after SyncWorker.submit(), the job status is "completed".
def test_job_completes_after_submit() -> None:
    raise NotImplementedError


# ── TODO 3 ───────────────────────────────────────────────────────────────────
# Test that a failing job (fn raises) stores error and has status "failed".
def test_failed_job_stores_error() -> None:
    raise NotImplementedError


# ── TODO 4 ───────────────────────────────────────────────────────────────────
# Test that job result is stored correctly after completion.
def test_job_result_stored() -> None:
    raise NotImplementedError


# ── TODO 5 ───────────────────────────────────────────────────────────────────
# Test that two separate jobs do not overwrite each other.
def test_two_jobs_are_independent() -> None:
    raise NotImplementedError


# ── TODO 6 ───────────────────────────────────────────────────────────────────
# Test that get() returns None for a nonexistent job_id.
def test_unknown_job_returns_none() -> None:
    raise NotImplementedError
