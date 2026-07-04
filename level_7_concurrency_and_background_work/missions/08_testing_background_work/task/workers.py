# task/workers.py
import threading
from typing import Any, Callable
from task.jobs import JobRepository, JobStatus


class BackgroundWorker:
    def __init__(self, repo: JobRepository) -> None:
        self._repo = repo

    def submit(self, job_id: str, fn: Callable[[], Any]) -> None:
        self._repo.set_status(job_id, JobStatus.running)
        thread = threading.Thread(target=self._run, args=(job_id, fn), daemon=True)
        thread.start()

    def _run(self, job_id: str, fn: Callable[[], Any]) -> None:
        try:
            result = fn()
            self._repo.set_result(job_id, result)
            self._repo.set_status(job_id, JobStatus.completed)
        except Exception as exc:
            self._repo.set_error(job_id, str(exc))
            self._repo.set_status(job_id, JobStatus.failed)


class SyncWorker:
    """Runs jobs inline (no threading). Use in tests for determinism."""
    def __init__(self, repo: JobRepository) -> None:
        self._repo = repo

    def submit(self, job_id: str, fn: Callable[[], Any]) -> None:
        self._repo.set_status(job_id, JobStatus.running)
        try:
            result = fn()
            self._repo.set_result(job_id, result)
            self._repo.set_status(job_id, JobStatus.completed)
        except Exception as exc:
            self._repo.set_error(job_id, str(exc))
            self._repo.set_status(job_id, JobStatus.failed)
