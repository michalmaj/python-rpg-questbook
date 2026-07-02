# level_6_api/missions/07_api_tests/task/routers/heroes.py
from fastapi import APIRouter, Depends

from task.dependencies import get_battle_service
from task.rpg.services import BattleService

router = APIRouter()


@router.get("/heroes/classes", response_model=list[str])
def list_hero_classes(
    service: BattleService = Depends(get_battle_service),
) -> list[str]:
    return service.get_hero_classes()
