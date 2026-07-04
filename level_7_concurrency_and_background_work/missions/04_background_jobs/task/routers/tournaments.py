import threading
import uuid
from fastapi import APIRouter, HTTPException
from task.schemas import JobStarted, JobOut, TournamentRequest
from task.rpg.repositories import MonsterRepository
from task.rpg.services import SimulationService
from pathlib import Path

router = APIRouter()

# Smell: global mutable dict — works but not testable or thread-safe enough for prod
_jobs: dict[str, dict] = {}

_DATA = Path(__file__).parent.parent / "data"
_svc = SimulationService(MonsterRepository(_DATA / "monsters.json"))


def _run_tournament(job_id: str, n: int) -> None:
    """Run in background thread."""
    _jobs[job_id]["status"] = "running"
    try:
        summary = _svc.simulate_tournament(n)
        _jobs[job_id]["result"] = summary.to_dict()
        _jobs[job_id]["status"] = "completed"
    except Exception as exc:
        _jobs[job_id]["error"] = str(exc)
        _jobs[job_id]["status"] = "failed"


# TODO 1: implement POST /tournaments
# - generate job_id = str(uuid.uuid4())
# - store _jobs[job_id] = {"status": "pending", "result": None, "error": None}
# - start threading.Thread(target=_run_tournament, args=(job_id, req.battles), daemon=True)
# - return JobStarted(job_id=job_id) with status_code=202
@router.post("/tournaments", status_code=202, response_model=JobStarted)
def start_tournament(req: TournamentRequest) -> JobStarted:
    raise NotImplementedError


# TODO 2: implement GET /jobs/{job_id}
# - look up _jobs.get(job_id)
# - raise HTTPException(404) if not found
# - return JobOut with all fields
@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: str) -> JobOut:
    raise NotImplementedError
