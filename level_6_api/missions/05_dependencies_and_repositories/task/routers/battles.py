# level_6_api/missions/05_dependencies_and_repositories/task/routers/battles.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from task.config import DATA_DIR
from task.rpg.domain import HeroClass
from task.rpg.repositories import MonsterRepository
from task.rpg.services import BattleService, create_hero

_service = BattleService(monster_repo=MonsterRepository(DATA_DIR / "monsters.json"))

router = APIRouter()


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


@router.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(req: BattleRequest) -> BattleResultOut:
    hero = create_hero(req.hero_name, req.hero_class)
    try:
        result = _service.simulate(hero, req.monster_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return BattleResultOut(**vars(result))
