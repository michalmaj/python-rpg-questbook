"""Boss Fight: Concurrent Tournament Runner — API routes.

Implement three endpoints:
  POST /tournaments          → 202 + job_id (starts background simulation)
  GET  /tournaments/{job_id} → job status + result when completed
  GET  /tournaments/{job_id}/report → Markdown report (text/plain) or 404/425
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from api.schemas import TournamentRequest, JobStarted, JobOut
from api.dependencies import get_job_repo, get_worker, get_simulation_service
from jobs.jobs import JobRepository, BackgroundWorker, JobStatus
from rpg.services import SimulationService
from rpg.domain import TournamentSummary

router = APIRouter()


# TODO 1: POST /tournaments — start a background tournament
# - job_id = str(uuid.uuid4())
# - job_repo.create(job_id)
# - worker.submit(job_id, lambda: svc.simulate_tournament(req.battles).to_dict())
# - return JobStarted(job_id=job_id), status_code=202
@router.post("/tournaments", status_code=202, response_model=JobStarted)
def start_tournament(
    req: TournamentRequest,
    job_repo: JobRepository = Depends(get_job_repo),
    worker: BackgroundWorker = Depends(get_worker),
    svc: SimulationService = Depends(get_simulation_service),
) -> JobStarted:
    raise NotImplementedError


# TODO 2: GET /tournaments/{job_id} — poll job status
# - job = job_repo.get(job_id)
# - raise HTTPException(404) if not found
# - return JobOut(job_id=job.id, status=job.status, result=job.result, error=job.error)
@router.get("/tournaments/{job_id}", response_model=JobOut)
def get_tournament(
    job_id: str,
    job_repo: JobRepository = Depends(get_job_repo),
) -> JobOut:
    raise NotImplementedError


# TODO 3: GET /tournaments/{job_id}/report — Markdown report
# - job = job_repo.get(job_id); 404 if not found
# - if job.status != "completed": raise HTTPException(425, "Job not completed yet")
# - summary = TournamentSummary(**job.result)
# - return PlainTextResponse(summary.to_markdown())
@router.get("/tournaments/{job_id}/report")
def get_report(
    job_id: str,
    job_repo: JobRepository = Depends(get_job_repo),
) -> PlainTextResponse:
    raise NotImplementedError
