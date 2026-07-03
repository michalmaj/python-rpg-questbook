# level_6_api/missions/07_api_tests/task/schemas.py
"""Shared Pydantic schemas for the RPG Battle API."""
from pydantic import BaseModel

from task.rpg.domain import HeroClass


class MonsterOut(BaseModel):
    name: str
    hp: int
    atk: int
    defense: int
    gold: int


class BattleRequest(BaseModel):
    hero_name: str
    hero_class: HeroClass
    monster_name: str


class BattleResultOut(BaseModel):
    hero_name: str
    monster_name: str
    winner: str
    rounds: int
    gold_earned: int


class ErrorOut(BaseModel):
    detail: str


class SessionCreated(BaseModel):
    session_id: str
