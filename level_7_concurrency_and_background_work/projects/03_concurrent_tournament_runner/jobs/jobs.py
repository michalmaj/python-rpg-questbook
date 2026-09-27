# jobs/jobs.py
import json
import os
import threading
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Protocol

# _simulate_one lives in the domain layer (rpg.services) so battle logic has
# one canonical home. It must stay module-level there to remain picklable.
from rpg.services import _simulate_one


def _run_battles(battles: int) -> dict:
    """Run `battles` simulations with random seeds; used by SyncWorker/BackgroundWorker."""
    seeds = [int.from_bytes(os.urandom(4), "big") for _ in range(battles)]
    results = [_simulate_one(s) for s in seeds]
    hero_wins = sum(1 for r in results if r["winner"] == "hero")
    return {
        "total_battles": battles,
        "hero_wins": hero_wins,
        "monster_wins": battles - hero_wins,
        "hero_win_rate": round(hero_wins / battles, 4) if battles else 0.0,
    }


# ── Job model ─────────────────────────────────────────────────────────────────

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


# ── Repository protocol + implementations ────────────────────────────────────

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
                job.status = JobStatus.completed

    def set_error(self, job_id: str, error: str) -> None:
        with self._lock:
            if job := self._jobs.get(job_id):
                job.error = error
                job.status = JobStatus.failed


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
                job.status = JobStatus.completed
                self._write(job)

    def set_error(self, job_id: str, error: str) -> None:
        with self._lock:
            if job := self._read(job_id):
                job.error = error
                job.status = JobStatus.failed
                self._write(job)


# ── Worker protocol + implementations ────────────────────────────────────────

class Worker(Protocol):
    """Accepts a job_id and the number of battles to simulate."""
    def submit(self, job_id: str, battles: int) -> None: ...


class SyncWorker:
    """Runs the simulation inline (no threading). Use in tests for determinism."""
    def __init__(self, repo: JobRepository) -> None:
        self._repo = repo

    def submit(self, job_id: str, battles: int) -> None:
        self._repo.set_status(job_id, JobStatus.running)
        try:
            result = _run_battles(battles)
            self._repo.set_result(job_id, result)
        except Exception as exc:
            self._repo.set_error(job_id, str(exc))


class BackgroundWorker:
    """Runs the simulation in a daemon background thread."""
    def __init__(self, repo: JobRepository) -> None:
        self._repo = repo

    def submit(self, job_id: str, battles: int) -> None:
        self._repo.set_status(job_id, JobStatus.running)
        thread = threading.Thread(target=self._run, args=(job_id, battles), daemon=True)
        thread.start()

    def _run(self, job_id: str, battles: int) -> None:
        try:
            result = _run_battles(battles)
            self._repo.set_result(job_id, result)
        except Exception as exc:
            self._repo.set_error(job_id, str(exc))


class ProcessPoolTournamentWorker:
    """Distributes individual battle simulations across CPU cores.

    Architecture:
      HTTP thread → background thread → ProcessPoolExecutor
                                        (pool.map distributes battles)

    Each worker process receives only `_simulate_one` (a top-level function,
    picklable by multiprocessing) and an integer seed. No closures or lambdas
    are sent across the process boundary.
    """

    def __init__(self, repo: JobRepository, workers: int = 4) -> None:
        self._repo = repo
        self._workers = workers

    def submit(self, job_id: str, battles: int) -> None:
        self._repo.set_status(job_id, JobStatus.running)
        thread = threading.Thread(
            target=self._run, args=(job_id, battles), daemon=True
        )
        thread.start()

    def _run(self, job_id: str, battles: int) -> None:
        try:
            seeds = [int.from_bytes(os.urandom(4), "big") for _ in range(battles)]
            with ProcessPoolExecutor(max_workers=self._workers) as pool:
                # pool.map sends _simulate_one + one integer seed to each worker process.
                # Both are picklable — this is the critical difference from pool.submit(lambda).
                results = list(pool.map(_simulate_one, seeds))
            hero_wins = sum(1 for r in results if r["winner"] == "hero")
            result = {
                "total_battles": battles,
                "hero_wins": hero_wins,
                "monster_wins": battles - hero_wins,
                "hero_win_rate": round(hero_wins / battles, 4) if battles else 0.0,
            }
            self._repo.set_result(job_id, result)
        except Exception as exc:
            self._repo.set_error(job_id, str(exc))
