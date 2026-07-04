from fastapi import APIRouter, Depends, HTTPException
from api.schemas import BattleRequest, BattleResultOut
from api.dependencies import get_monster_repo
from rpg.repositories import MonsterRepository
from rpg.services import BattleService, create_hero

router = APIRouter()


@router.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(
    req: BattleRequest,
    repo: MonsterRepository = Depends(get_monster_repo),
) -> BattleResultOut:
    svc = BattleService(repo)
    hero = create_hero(req.hero_name, req.hero_class)
    try:
        result = svc.simulate(hero, req.monster_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return BattleResultOut(
        hero_name=result.hero_name,
        monster_name=result.monster_name,
        winner=result.winner,
        rounds=result.rounds,
        gold_earned=result.gold_earned,
    )
