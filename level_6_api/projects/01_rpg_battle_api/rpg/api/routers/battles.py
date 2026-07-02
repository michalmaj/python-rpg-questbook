"""Battles router."""
from fastapi import APIRouter

router = APIRouter()

# TODO: Add POST /battle/simulate endpoint
# It should accept a BattleRequest body and return BattleResultOut.
# Raise HTTPException(status_code=404) if the monster is not found.
#
# Steps:
#   1. Import Depends, HTTPException from fastapi
#   2. Import get_battle_service from rpg.api.dependencies
#   3. Import BattleRequest, BattleResultOut from rpg.api.schemas
#   4. Import BattleService from rpg.services
#   5. Import Hero from rpg.domain
#
# Example shape:
#   @router.post("/battle/simulate", response_model=BattleResultOut)
#   def simulate_battle(
#       req: BattleRequest,
#       service: BattleService = Depends(get_battle_service),
#   ):
#       hero = Hero(name=req.hero_name, hero_class=req.hero_class, ...)
#       try:
#           result = service.simulate(hero, req.monster_name)
#       except ValueError as exc:
#           raise HTTPException(status_code=404, detail=str(exc))
#       return result
#
# Tip: use rpg.services.create_hero(req.hero_name, req.hero_class) to build the Hero.
