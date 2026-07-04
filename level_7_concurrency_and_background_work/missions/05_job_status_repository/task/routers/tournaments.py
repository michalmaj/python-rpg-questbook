import uuid
from fastapi import APIRouter, Depends, HTTPException
from task.schemas import JobStarted, JobOut, TournamentRequest
from task.jobs import JobRepository
from task.workers import BackgroundWorker
from task.dependencies import get_job_repo, get_worker, get_simulation_service
from task.rpg.services import SimulationService

router = APIRouter()


# TODO: Refactor POST /tournaments to use JobRepository + BackgroundWorker
# (remove the global _jobs dict from M04)
@router.post("/tournaments", status_code=202, response_model=JobStarted)
def start_tournament(
    req: TournamentRequest,
    job_repo: JobRepository = Depends(get_job_repo),
    worker: BackgroundWorker = Depends(get_worker),
    svc: SimulationService = Depends(get_simulation_service),
) -> JobStarted:
    raise NotImplementedError


@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(
    job_id: str,
    job_repo: JobRepository = Depends(get_job_repo),
) -> JobOut:
    raise NotImplementedError
