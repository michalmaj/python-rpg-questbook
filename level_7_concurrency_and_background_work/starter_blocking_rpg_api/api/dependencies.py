from functools import lru_cache
from pathlib import Path
from rpg.repositories import MonsterRepository
from rpg.services import SimulationService

_DATA = Path(__file__).parent.parent / "data"


@lru_cache
def get_monster_repo() -> MonsterRepository:
    return MonsterRepository(_DATA / "monsters.json")


def get_simulation_service() -> SimulationService:
    return SimulationService(get_monster_repo())
