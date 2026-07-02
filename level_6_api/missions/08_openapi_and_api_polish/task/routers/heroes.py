# level_6_api/missions/08_openapi_and_api_polish/task/routers/heroes.py
from fastapi import APIRouter, Depends

from task.dependencies import get_battle_service
from task.rpg.services import BattleService

router = APIRouter()


# TODO 3: Add a summary argument to this endpoint decorator.
@router.get("/heroes/classes", response_model=list[str])
def list_hero_classes(
    service: BattleService = Depends(get_battle_service),
) -> list[str]:
    return service.get_hero_classes()
