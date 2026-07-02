"""Monsters router."""
from fastapi import APIRouter

router = APIRouter()

# TODO: Add GET /monsters endpoint
# It should return a list of MonsterOut (all monsters from the repository).
#
# Steps:
#   1. Import Depends from fastapi
#   2. Import get_battle_service from rpg.api.dependencies
#   3. Import MonsterOut from rpg.api.schemas
#   4. Import BattleService from rpg.services
#
# Example shape:
#   @router.get("/monsters", response_model=list[MonsterOut])
#   def list_monsters(service: BattleService = Depends(get_battle_service)):
#       return service.get_available_monsters()
