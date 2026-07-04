from fastapi import APIRouter, Depends
from task.schemas import TournamentRequest, TournamentOut
from task.dependencies import get_simulation_service
from task.rpg.services import SimulationService

router = APIRouter()


# TODO: Convert to async def. Observe: it still blocks because simulate_tournament
# is CPU-bound. async def only helps for I/O-bound work (DB, HTTP calls, file reads).
@router.post("/tournaments", response_model=TournamentOut)
def run_tournament(
    req: TournamentRequest,
    svc: SimulationService = Depends(get_simulation_service),
) -> TournamentOut:
    summary = svc.simulate_tournament(req.battles)
    return TournamentOut(**summary.to_dict())
