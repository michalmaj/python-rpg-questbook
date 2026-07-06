"""Heroes router."""
from fastapi import APIRouter

router = APIRouter()

# TODO: Add GET /heroes/classes endpoint
# It should return a list of hero class name strings.
#
# Steps:
#   1. Import Depends from fastapi
#   2. Import get_battle_service from rpg.api.dependencies
#   3. Import BattleService from rpg.services
#
# Example shape:
#   @router.get("/heroes/classes", response_model=list[str])
#   def list_hero_classes(service: BattleService = Depends(get_battle_service)):
#       return service.get_hero_classes()
