# level_6_api/missions/05_dependencies_and_repositories/task/routers/monsters.py
from fastapi import APIRouter
from pydantic import BaseModel

from task.config import DATA_DIR
from task.rpg.repositories import MonsterRepository
from task.rpg.services import BattleService

# Smell: service created manually in each router module
_service = BattleService(monster_repo=MonsterRepository(DATA_DIR / "monsters.json"))

router = APIRouter()


class MonsterOut(BaseModel):
    name: str
    hp: int
    atk: int
    def_: int
    gold: int


@router.get("/monsters", response_model=list[MonsterOut])
def list_monsters() -> list[MonsterOut]:
    return [MonsterOut(**vars(m)) for m in _service.get_available_monsters()]
