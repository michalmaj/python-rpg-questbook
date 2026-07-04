from fastapi import APIRouter, Depends
from api.schemas import TournamentRequest, TournamentOut
from api.dependencies import get_simulation_service
from rpg.services import SimulationService

router = APIRouter()


@router.post("/tournaments", response_model=TournamentOut)
def run_tournament(
    req: TournamentRequest,
    svc: SimulationService = Depends(get_simulation_service),
) -> TournamentOut:
    summary = svc.simulate_tournament(req.battles)  # BLOCKS until done
    return TournamentOut(
        total_battles=summary.total_battles,
        hero_wins=summary.hero_wins,
        monster_wins=summary.monster_wins,
        hero_win_rate=summary.hero_win_rate,
    )
