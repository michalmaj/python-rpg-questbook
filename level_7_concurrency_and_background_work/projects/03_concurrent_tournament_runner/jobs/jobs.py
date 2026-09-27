# jobs/jobs.py
import json
import random
import threading
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Protocol


# ── Battle simulation data ────────────────────────────────────────────────────
# Embedded here so _simulate_one is fully self-contained and picklable.
_HERO_STATS: dict[str, dict[str, int]] = {
    "warrior": {"hp": 120, "atk": 12, "def_": 6},
    "mage":    {"hp": 80,  "atk": 18, "def_": 2},
    "rogue":   {"hp": 100, "atk": 15, "def_": 4},
}
_MONSTERS_DATA: list[dict[str, int]] = [
    {"hp": 30,  "atk": 8,  "def_": 2},  # Goblin
    {"hp": 60,  "atk": 12, "def_": 4},  # Orc
    {"hp": 150, "atk": 20, "def_": 8},  # Dragon
]


def _simulate_one(seed: int) -> dict:
    """Simulate one battle deterministically from seed.

    Module-level so ProcessPoolExecutor can pickle it. Never refactor into a
    lambda or nested function — pickling requires a top-level name.
    Returns {"winner": "hero" | "monster", "rounds": int}.
    """
    rng = random.Random(seed)
    hero_class = rng.choice(list(_HERO_STATS.keys()))
    stats = _HERO_STATS[hero_class]
    hero_hp, hero_atk, hero_def = stats["hp"], stats["atk"], stats["def_"]
    m = dict(rng.choice(_MONSTERS_DATA))
    rounds = 0
    while hero_hp > 0 and m["hp"] > 0:
        rounds += 1
        m["hp"] = max(0, m["hp"] - max(1, hero_atk + rng.randint(1, 6) - m["def_"]))
        if m["hp"] <= 0:
            return {"winner": "hero", "rounds": rounds}
        hero_hp = max(0, hero_hp - max(1, m["atk"] + rng.randint(1, 6) - hero_def))
    return {"winner": "monster", "rounds": rounds}


def _run_battles(battles: int) -> dict:
    """Run `battles` simulations sequentially; used by SyncWorker/BackgroundWorker."""
    results = [_simulate_one(i) for i in range(battles)]
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
            with ProcessPoolExecutor(max_workers=self._workers) as pool:
                # pool.map sends _simulate_one + an integer to each worker process.
                # Both are picklable — this is the critical difference from pool.submit(lambda).
                results = list(pool.map(_simulate_one, range(battles)))
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
