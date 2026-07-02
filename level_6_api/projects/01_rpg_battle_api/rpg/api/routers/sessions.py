"""Sessions and reports router."""
from fastapi import APIRouter

router = APIRouter()

# TODO: Implement three endpoints:
#
# 1. POST /sessions — simulate a battle and persist the result
#    - Accept a BattleRequest body
#    - Simulate the battle (use get_battle_service)
#    - Generate a UUID session_id (import uuid; session_id = str(uuid.uuid4()))
#    - Save result via session_repo.save(session_id, result)
#    - Return {"session_id": session_id} with status_code=201
#
# 2. GET /sessions/{session_id} — retrieve a stored battle result
#    - Look up result = session_repo.get(session_id)
#    - If None: raise HTTPException(status_code=404, detail="Session not found")
#    - Return result as BattleResultOut
#
# 3. GET /reports/{session_id} — retrieve a Markdown battle report
#    - Look up result = session_repo.get(session_id)
#    - If None: raise HTTPException(status_code=404, detail="Session not found")
#    - Return result.to_markdown() as plain text
#    - Hint: from fastapi.responses import PlainTextResponse
#            return PlainTextResponse(result.to_markdown())
#
# Imports you will need:
#   import uuid
#   from fastapi import APIRouter, Depends, HTTPException
#   from fastapi.responses import PlainTextResponse
#   from rpg.api.dependencies import get_battle_service, get_session_repo
#   from rpg.api.schemas import BattleRequest, BattleResultOut, SessionCreated
#   from rpg.repositories import SessionRepository
#   from rpg.services import BattleService, create_hero
