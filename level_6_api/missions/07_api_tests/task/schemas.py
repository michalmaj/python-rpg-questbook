# level_6_api/missions/07_api_tests/task/schemas.py
"""Shared Pydantic schemas for the RPG Battle API."""
from pydantic import BaseModel


class MonsterOut(BaseModel):
    name: str
    hp: int
    atk: int
    def_: int
    gold: int


class BattleRequest(BaseModel):
    hero_name: str
    hero_class: str
    monster_name: str


class BattleResultOut(BaseModel):
    hero_name: str
    monster_name: str
    winner: str
    rounds: int
    gold_earned: int


class ErrorOut(BaseModel):
    detail: str
