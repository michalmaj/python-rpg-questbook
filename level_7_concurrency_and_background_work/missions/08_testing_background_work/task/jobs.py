# task/jobs.py
import json
import threading
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
