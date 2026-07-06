# jobs/jobs.py
import json
import threading
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Protocol


class JobStatus(StrEnum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


@dataclass
class Job:
    id: str
    status: JobStatus
    result: dict | None = None
    error: str | None = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class JobRepository(Protocol):
    def create(self, job_id: str) -> Job: ...
    def get(self, job_id: str) -> Job | None: ...
    def set_status(self, job_id: str, status: JobStatus) -> None: ...
    def set_result(self, job_id: str, result: dict) -> None: ...
    def set_error(self, job_id: str, error: str) -> None: ...


class Worker(Protocol):
    def submit(self, job_id: str, fn: Callable[[], Any]) -> None: ...


class InMemoryJobRepository:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def create(self, job_id: str) -> Job:
        job = Job(id=job_id, status=JobStatus.pending)
        with self._lock:
            self._jobs[job_id] = job
        return job

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def set_status(self, job_id: str, status: JobStatus) -> None:
        with self._lock:
            if job := self._jobs.get(job_id):
                job.status = status

    def set_result(self, job_id: str, result: dict) -> None:
        with self._lock:
            if job := self._jobs.get(job_id):
                job.result = result

    def set_error(self, job_id: str, error: str) -> None:
        with self._lock:
            if job := self._jobs.get(job_id):
                job.error = error


class JsonJobRepository:
    def __init__(self, jobs_dir: Path) -> None:
        self._dir = jobs_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _path(self, job_id: str) -> Path:
        return self._dir / f"{job_id}.json"

    def _read(self, job_id: str) -> Job | None:
        p = self._path(job_id)
        if not p.exists():
            return None
        data = json.loads(p.read_text())
        return Job(
            id=data["id"],
            status=JobStatus(data["status"]),
            result=data.get("result"),
            error=data.get("error"),
            created_at=data["created_at"],
        )

    def _write(self, job: Job) -> None:
        self._path(job.id).write_text(json.dumps({
            "id": job.id,
            "status": job.status,
            "result": job.result,
            "error": job.error,
            "created_at": job.created_at,
        }))

    def create(self, job_id: str) -> Job:
        job = Job(id=job_id, status=JobStatus.pending)
        with self._lock:
            self._write(job)
        return job

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._read(job_id)

    def set_status(self, job_id: str, status: JobStatus) -> None:
        with self._lock:
            if job := self._read(job_id):
                job.status = status
                self._write(job)

    def set_result(self, job_id: str, result: dict) -> None:
        with self._lock:
            if job := self._read(job_id):
                job.result = result
                self._write(job)

    def set_error(self, job_id: str, error: str) -> None:
        with self._lock:
            if job := self._read(job_id):
                job.error = error
                self._write(job)


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


class ProcessPoolTournamentWorker:
    """Runs the tournament in a background thread.

    Inside that thread, uses ProcessPoolExecutor to parallelize individual
    battle simulations across CPU cores — same Worker Protocol interface,
    faster for CPU-bound work.
    """

    def __init__(self, repo: JobRepository, workers: int = 4) -> None:
        self._repo = repo
        self._workers = workers

    def submit(self, job_id: str, fn: Callable[[], Any]) -> None:
        self._repo.set_status(job_id, JobStatus.running)
        thread = threading.Thread(
            target=self._run, args=(job_id, fn), daemon=True
        )
        thread.start()

    def _run(self, job_id: str, fn: Callable[[], Any]) -> None:
        try:
            with ProcessPoolExecutor(max_workers=self._workers) as pool:
                future = pool.submit(fn)
                result = future.result()
            self._repo.set_result(job_id, result)
            self._repo.set_status(job_id, JobStatus.completed)
        except Exception as exc:
            self._repo.set_error(job_id, str(exc))
            self._repo.set_status(job_id, JobStatus.failed)
