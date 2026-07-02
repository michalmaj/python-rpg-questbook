# level_6_api/missions/06_api_errors_and_status_codes/task/dependencies.py
"""Dependency providers for FastAPI Depends()."""
from fastapi import Depends

from task.config import DATA_DIR
from task.rpg.repositories import MonsterRepository, SessionRepository
from task.rpg.services import BattleService


def get_monster_repo() -> MonsterRepository:
    return MonsterRepository(DATA_DIR / "monsters.json")


def get_session_repo() -> SessionRepository:
    return SessionRepository(DATA_DIR / "sessions")


def get_battle_service(
    repo: MonsterRepository = Depends(get_monster_repo),
) -> BattleService:
    return BattleService(monster_repo=repo)
