"""Mission 02: Request/Response Schemas.

Goal:  Add Pydantic models for API inputs and outputs.
       API schemas are always separate from domain dataclasses.
Check: uv run python check.py
"""
from pathlib import Path

from fastapi import FastAPI
from rpg.domain import HeroClass
from rpg.repositories import MonsterRepository
from rpg.services import BattleService, create_hero

_DATA = Path(__file__).parent / "data"
_service = BattleService(monster_repo=MonsterRepository(_DATA / "monsters.json"))

app = FastAPI(title="RPG Battle API", version="1.0")

# TODO 1: Import BaseModel from pydantic
# from pydantic import BaseModel

# TODO 2: Define MonsterOut schema (separate from rpg.domain.Monster)
# class MonsterOut(BaseModel):
#     name: str
#     hp: int
#     atk: int
#     def_: int
#     gold: int

# TODO 3: Define BattleRequest schema
# class BattleRequest(BaseModel):
#     hero_name: str
#     hero_class: HeroClass
#     monster_name: str

# TODO 4: Define BattleResultOut schema
# class BattleResultOut(BaseModel):
#     hero_name: str
#     monster_name: str
#     winner: str
#     rounds: int
#     gold_earned: int


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# TODO 5: Update to return list[MonsterOut] with response_model=list[MonsterOut]
@app.get("/monsters")
def list_monsters() -> list[str]:
    return [m.name for m in _service.get_available_monsters()]


# TODO 6: Add POST /battle/simulate
# Takes BattleRequest body, returns BattleResultOut
# Use create_hero(req.hero_name, req.hero_class) then _service.simulate(hero, req.monster_name)
# Hint: BattleResult has the same fields as BattleResultOut — use dataclasses.asdict() or construct manually
