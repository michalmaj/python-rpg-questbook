from pydantic import BaseModel, Field
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


class TournamentRequest(BaseModel):
    battles: int = Field(gt=0, le=1_000_000, description="Number of battles to simulate")


class TournamentOut(BaseModel):
    total_battles: int
    hero_wins: int
    monster_wins: int
    hero_win_rate: float
