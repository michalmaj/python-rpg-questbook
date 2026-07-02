# level_6_api/missions/06_api_errors_and_status_codes/task/routers/heroes.py
from fastapi import APIRouter

router = APIRouter()

# TODO: Add GET /heroes/classes
# Returns list[str] of available hero class names
# Use BattleService = Depends(get_battle_service) and call service.get_hero_classes()
# This endpoint cannot fail — no error handling needed here
