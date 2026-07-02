"""Mission 03: Routes Call Services.

Goal:  Thin routes — all business logic belongs in the service layer.
       The endpoint below has a smell: combat logic lives inside the function.
       Refactor it so the endpoint only calls _service.simulate().
Check: uv run python check.py
"""
import copy
import random
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rpg.domain import Hero, HeroClass
from rpg.repositories import MonsterRepository
from rpg.services import BattleService

_DATA = Path(__file__).parent / "data"
_service = BattleService(monster_repo=MonsterRepository(_DATA / "monsters.json"))

app = FastAPI(title="RPG Battle API", version="1.0")


class MonsterOut(BaseModel):
    name: str
    hp: int
    atk: int
    def_: int
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


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/monsters", response_model=list[MonsterOut])
def list_monsters() -> list[MonsterOut]:
    return [MonsterOut(**vars(m)) for m in _service.get_available_monsters()]


# Smell: combat simulation logic lives inside the endpoint function.
# TODO: Refactor so this endpoint calls _service.simulate(hero, req.monster_name)
#       and builds BattleResultOut from the returned BattleResult.
#       After refactoring, random.randint and copy.deepcopy must be gone from this file.
@app.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(req: BattleRequest) -> BattleResultOut:
    monsters = _service.get_available_monsters()
    monster = next((m for m in monsters if m.name.lower() == req.monster_name.lower()), None)
    if monster is None:
        raise HTTPException(status_code=404, detail="Monster not found")
    monster = copy.deepcopy(monster)
    hero = Hero(
        name=req.hero_name, hero_class=req.hero_class,
        hp=120, max_hp=120, atk=12, def_=6,
    )
    rounds = 0
    while hero.hp > 0 and monster.hp > 0:
        rounds += 1
        dmg = max(1, hero.atk + random.randint(1, 6) - monster.def_)
        monster.take_damage(dmg)
        if not monster.is_alive:
            return BattleResultOut(
                hero_name=hero.name, monster_name=monster.name,
                winner="hero", rounds=rounds, gold_earned=monster.gold,
            )
        hero.hp = max(0, hero.hp - max(1, monster.atk + random.randint(1, 6) - hero.def_))
    return BattleResultOut(
        hero_name=hero.name, monster_name=monster.name,
        winner="monster", rounds=rounds, gold_earned=0,
    )
