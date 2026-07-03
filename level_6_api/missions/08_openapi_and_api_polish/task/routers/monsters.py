# level_6_api/missions/08_openapi_and_api_polish/task/routers/monsters.py
from fastapi import APIRouter, Depends, HTTPException

from task.dependencies import get_battle_service, get_monster_repo
from task.rpg.repositories import MonsterRepository
from task.rpg.services import BattleService
from task.schemas import MonsterOut

router = APIRouter()


# TODO 3: Add a summary argument to each endpoint decorator.
# Open README.md for examples.
@router.get("/monsters", response_model=list[MonsterOut])
def list_monsters(
    service: BattleService = Depends(get_battle_service),
) -> list[MonsterOut]:
    return [MonsterOut(name=m.name, hp=m.hp, atk=m.atk, defense=m.def_, gold=m.gold) for m in service.get_available_monsters()]


@router.get("/monsters/{name}", response_model=MonsterOut)
def get_monster(
    name: str,
    repo: MonsterRepository = Depends(get_monster_repo),
) -> MonsterOut:
    monster = repo.get(name)
    if monster is None:
        raise HTTPException(status_code=404, detail=f"Monster '{name}' not found")
    return MonsterOut(name=monster.name, hp=monster.hp, atk=monster.atk, defense=monster.def_, gold=monster.gold)
