# level_6_api/missions/06_api_errors_and_status_codes/task/routers/sessions.py
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from task.dependencies import get_battle_service, get_session_repo
from task.rpg.domain import HeroClass
from task.rpg.repositories import SessionRepository
from task.rpg.services import BattleService, create_hero
from task.schemas import BattleResultOut

router = APIRouter()


class BattleRequest(BaseModel):
    hero_name: str
    hero_class: HeroClass
    monster_name: str


@router.post("/sessions", status_code=201)
def create_session(
    req: BattleRequest,
    service: BattleService = Depends(get_battle_service),
    session_repo: SessionRepository = Depends(get_session_repo),
) -> dict:
    hero = create_hero(req.hero_name, req.hero_class)
    try:
        result = service.simulate(hero, req.monster_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    session_id = str(uuid.uuid4())
    session_repo.save(session_id, result)
    return {"session_id": session_id}


@router.get("/sessions/{session_id}", response_model=BattleResultOut)
def get_session(
    session_id: str,
    session_repo: SessionRepository = Depends(get_session_repo),
) -> BattleResultOut:
    result = session_repo.get(session_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return BattleResultOut(**vars(result))
