from fastapi import APIRouter, Depends, HTTPException
from task.schemas import MonsterOut
from task.dependencies import get_monster_repo
from task.rpg.repositories import MonsterRepository

router = APIRouter()


@router.get("/monsters", response_model=list[MonsterOut])
async def list_monsters(repo: MonsterRepository = Depends(get_monster_repo)) -> list[MonsterOut]:
    return [MonsterOut(name=m.name, hp=m.hp, atk=m.atk, defense=m.def_, gold=m.gold)
            for m in repo.list_all()]


@router.get("/monsters/{name}", response_model=MonsterOut)
async def get_monster(name: str, repo: MonsterRepository = Depends(get_monster_repo)) -> MonsterOut:
    m = repo.get(name)
    if m is None:
        raise HTTPException(status_code=404, detail=f"Monster '{name}' not found")
    return MonsterOut(name=m.name, hp=m.hp, atk=m.atk, defense=m.def_, gold=m.gold)
