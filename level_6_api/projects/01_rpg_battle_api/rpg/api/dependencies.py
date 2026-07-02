"""Dependency factories for FastAPI Depends()."""
from pathlib import Path

# DATA_DIR = Path(__file__).parents[2] / "data"
# SESSIONS_DIR = Path(__file__).parents[2] / "data" / "sessions"

# TODO: implement get_monster_repo() -> MonsterRepository
#   Returns: MonsterRepository(DATA_DIR / "monsters.json")
#
# TODO: implement get_session_repo() -> SessionRepository
#   Returns: SessionRepository(SESSIONS_DIR)
#
# TODO: implement get_battle_service(repo = Depends(get_monster_repo)) -> BattleService
#   Returns: BattleService(monster_repo=repo)
#
# Hint: from fastapi import Depends
# Hint: from rpg.repositories import MonsterRepository, SessionRepository
# Hint: from rpg.services import BattleService


def get_session_repo():  # type: ignore[return]
    raise NotImplementedError("Implement get_session_repo() in dependencies.py")
