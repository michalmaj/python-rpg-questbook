# level_6_api/missions/07_api_tests/task/routers/battles.py
from fastapi import APIRouter, Depends, HTTPException

from task.dependencies import get_battle_service
from task.rpg.services import BattleService, create_hero
from task.schemas import BattleRequest, BattleResultOut

router = APIRouter()


@router.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(
    req: BattleRequest,
    service: BattleService = Depends(get_battle_service),
) -> BattleResultOut:
    hero = create_hero(req.hero_name, req.hero_class)
    try:
        result = service.simulate(hero, req.monster_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return BattleResultOut(**vars(result))
