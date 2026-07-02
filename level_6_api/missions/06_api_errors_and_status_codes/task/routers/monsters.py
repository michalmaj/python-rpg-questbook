# level_6_api/missions/06_api_errors_and_status_codes/task/routers/monsters.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from task.dependencies import get_battle_service
from task.rpg.services import BattleService

router = APIRouter()


class MonsterOut(BaseModel):
    name: str
    hp: int
    atk: int
    def_: int
    gold: int


@router.get("/monsters", response_model=list[MonsterOut])
def list_monsters(
    service: BattleService = Depends(get_battle_service),
) -> list[MonsterOut]:
    return [MonsterOut(**vars(m)) for m in service.get_available_monsters()]
