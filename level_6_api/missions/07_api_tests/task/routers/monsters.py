# level_6_api/missions/07_api_tests/task/routers/monsters.py
from fastapi import APIRouter, Depends, HTTPException

from task.dependencies import get_battle_service, get_monster_repo
from task.rpg.repositories import MonsterRepository
from task.rpg.services import BattleService
from task.schemas import MonsterOut

router = APIRouter()


@router.get("/monsters", response_model=list[MonsterOut])
def list_monsters(
    service: BattleService = Depends(get_battle_service),
) -> list[MonsterOut]:
    return [MonsterOut(**vars(m)) for m in service.get_available_monsters()]


@router.get("/monsters/{name}", response_model=MonsterOut)
def get_monster(
    name: str,
    repo: MonsterRepository = Depends(get_monster_repo),
) -> MonsterOut:
    monster = repo.get(name)
    if monster is None:
        raise HTTPException(status_code=404, detail=f"Monster '{name}' not found")
    return MonsterOut(**vars(monster))
