# level_6_api/missions/05_dependencies_and_repositories/task/routers/sessions.py
"""Session endpoints — student implements using Depends()."""
from fastapi import APIRouter

router = APIRouter()

# TODO 1: Create task/dependencies.py with:
#   def get_monster_repo() -> MonsterRepository
#   def get_session_repo() -> SessionRepository
#   def get_battle_service(repo=Depends(get_monster_repo)) -> BattleService

# TODO 2: Refactor monsters.py and battles.py to use Depends() instead of _service module variable

# TODO 3: Add POST /sessions endpoint here
#   Body: BattleRequest (same fields as battles.py)
#   - Simulate battle using BattleService = Depends(get_battle_service)
#   - Save result with SessionRepository = Depends(get_session_repo)
#   - Return {"session_id": "<uuid>"} with status_code=201

# TODO 4: Add GET /sessions/{session_id} endpoint
#   - Load session from SessionRepository
#   - Return BattleResultOut, or 404 if not found
