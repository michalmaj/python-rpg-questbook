# level_6_api/missions/01_first_fastapi_app/task.py
"""Mission 01: First FastAPI App.

Goal:  Create a FastAPI app with two endpoints.
Run:   uv run uvicorn task:app --reload  (from this folder)
Docs:  http://127.0.0.1:8000/docs
Check: uv run python check.py
"""
from pathlib import Path

from rpg.repositories import MonsterRepository
from rpg.services import BattleService

_DATA = Path(__file__).parent / "data"
_service = BattleService(monster_repo=MonsterRepository(_DATA / "monsters.json"))

# TODO 1: Import FastAPI
# from fastapi import FastAPI

# TODO 2: Create the app
# app = FastAPI(title="RPG Battle API", version="1.0")

# TODO 3: Add GET /health endpoint
# Returns: {"status": "ok"}

# TODO 4: Add GET /monsters endpoint
# Use _service.get_available_monsters() to get the list
# Return a plain list of monster names: list[str]
