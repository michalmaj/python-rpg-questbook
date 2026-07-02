# level_6_api/missions/04_api_routers/task/main.py
"""Mission 04: API Routers.

Goal:  Split endpoint functions into separate APIRouter modules.
Run:   uv run uvicorn task.main:app --reload  (from mission folder)
Check: uv run python check.py
"""
from fastapi import FastAPI

app = FastAPI(title="RPG Battle API", version="1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# TODO 1: Create task/routers/__init__.py (empty)
# TODO 2: Create task/routers/monsters.py
#   - from fastapi import APIRouter
#   - router = APIRouter()
#   - GET /monsters → list[MonsterOut]
#   - Use task.config.DATA_DIR and task.rpg.services.BattleService
#
# TODO 3: Create task/routers/battles.py
#   - router = APIRouter()
#   - POST /battle/simulate → BattleResultOut
#
# TODO 4: Include both routers in this file
# from task.routers import monsters, battles
# app.include_router(monsters.router)
# app.include_router(battles.router)
