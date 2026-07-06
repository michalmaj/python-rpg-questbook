"""Job queue: repository + workers for the Background Report Queue.

Your task: implement BackgroundWorker.

Do NOT modify InMemoryJobRepository or SyncWorker — they are pre-built
and used by check.py to test your implementation deterministically.
"""

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable


# ── Domain ────────────────────────────────────────────────────────────────────

@dataclass
class Job:
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"   # "pending" | "running" | "completed" | "failed"
    result: dict | None = None
    error: str | None = None


# ── Pre-implemented: in-memory repository ────────────────────────────────────

class InMemoryJobRepository:
    """Thread-safe in-memory job store. Do not modify."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def create(self) -> Job:
        job = Job()
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def set_status(self, job_id: str, status: str) -> None:
        with self._lock:
            if job := self._jobs.get(job_id):
                job.status = status

    def set_result(self, job_id: str, result: dict) -> None:
        with self._lock:
            if job := self._jobs.get(job_id):
                job.result = result
                job.status = "completed"

    def set_error(self, job_id: str, error: str) -> None:
        with self._lock:
            if job := self._jobs.get(job_id):
                job.error = error
                job.status = "failed"


# ── Pre-implemented: sync worker (for tests) ─────────────────────────────────

class SyncWorker:
    """Runs jobs inline — no threads. Use in tests for determinism. Do not modify."""

    def __init__(self, repo: InMemoryJobRepository) -> None:
        self._repo = repo

    def submit(self, job_id: str, fn: Callable[[], Any]) -> None:
        self._repo.set_status(job_id, "running")
        try:
            result = fn()
            self._repo.set_result(job_id, result)
        except Exception as exc:
            self._repo.set_error(job_id, str(exc))


# ── Your implementation ───────────────────────────────────────────────────────

class BackgroundWorker:
    """Runs jobs in a daemon thread so the API stays responsive.

    Requirements:
        - __init__ accepts a repo: InMemoryJobRepository
        - submit(job_id, fn) sets status to "running", then executes fn()
          in a daemon thread
        - On success: call repo.set_result(job_id, result)
        - On exception: call repo.set_error(job_id, str(exc))
        - The API must return the 202 response BEFORE fn() completes
    """

    def __init__(self, repo: InMemoryJobRepository) -> None:
        self._repo = repo

    def submit(self, job_id: str, fn: Callable[[], Any]) -> None:
        raise NotImplementedError
