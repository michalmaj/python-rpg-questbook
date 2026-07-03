"""API Pydantic schemas — separate from domain dataclasses."""
from pydantic import BaseModel

from rpg.domain import HeroClass


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


class SessionCreated(BaseModel):
    session_id: str
