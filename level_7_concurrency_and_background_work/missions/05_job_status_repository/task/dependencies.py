from functools import lru_cache
from pathlib import Path
from task.rpg.repositories import MonsterRepository
from task.rpg.services import SimulationService
from task.jobs import InMemoryJobRepository, JobRepository
from task.workers import BackgroundWorker

_DATA = Path(__file__).parent / "data"

_job_repo = InMemoryJobRepository()
_worker = BackgroundWorker(_job_repo)


@lru_cache
def get_monster_repo() -> MonsterRepository:
    return MonsterRepository(_DATA / "monsters.json")


def get_simulation_service() -> SimulationService:
    return SimulationService(get_monster_repo())


def get_job_repo() -> JobRepository:
    return _job_repo


def get_worker() -> BackgroundWorker:
    return _worker
