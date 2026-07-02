# level_6_api/missions/06_api_errors_and_status_codes/task/routers/battles.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from task.dependencies import get_battle_service
from task.rpg.domain import HeroClass
from task.rpg.services import BattleService, create_hero
from task.schemas import BattleResultOut

router = APIRouter()


class BattleRequest(BaseModel):
    hero_name: str
    hero_class: HeroClass
    monster_name: str


# TODO: Add ErrorOut schema to task/schemas.py with a `detail: str` field
# TODO: Import HTTPException from fastapi
# TODO: Catch ValueError from service.simulate() and raise HTTPException(status_code=404, ...)
@router.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(
    req: BattleRequest,
    service: BattleService = Depends(get_battle_service),
) -> BattleResultOut:
    hero = create_hero(req.hero_name, req.hero_class)
    result = service.simulate(hero, req.monster_name)  # raises ValueError if monster unknown
    return BattleResultOut(**vars(result))
