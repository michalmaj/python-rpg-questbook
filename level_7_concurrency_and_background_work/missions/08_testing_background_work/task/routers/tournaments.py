import uuid
from fastapi import APIRouter, Depends, HTTPException
from task.schemas import JobStarted, JobOut, TournamentRequest
from task.jobs import JobRepository
from task.workers import BackgroundWorker
from task.dependencies import get_job_repo, get_worker, get_simulation_service
from task.rpg.services import SimulationService

router = APIRouter()


@router.post("/tournaments", status_code=202, response_model=JobStarted)
def start_tournament(
    req: TournamentRequest,
    job_repo: JobRepository = Depends(get_job_repo),
    worker: BackgroundWorker = Depends(get_worker),
    svc: SimulationService = Depends(get_simulation_service),
) -> JobStarted:
    job_id = str(uuid.uuid4())
    job_repo.create(job_id)
    worker.submit(job_id, lambda: svc.simulate_tournament(req.battles).to_dict())
    return JobStarted(job_id=job_id)


@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(
    job_id: str,
    job_repo: JobRepository = Depends(get_job_repo),
) -> JobOut:
    job = job_repo.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")
    return JobOut(job_id=job.id, status=job.status, result=job.result, error=job.error)
