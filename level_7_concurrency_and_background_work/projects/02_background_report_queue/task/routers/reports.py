"""Reports router — POST /reports and GET /reports/{job_id}.

Pre-implemented — do not modify this file.
"""

from fastapi import APIRouter, Depends, HTTPException

from task.dependencies import get_repo, get_worker
from task.jobs import BackgroundWorker, InMemoryJobRepository
from task.report import compute_report
from task.schemas import ReportJob, ReportRequest, ReportResult

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", status_code=202)
def start_report(
    body: ReportRequest,
    repo: InMemoryJobRepository = Depends(get_repo),
    worker: BackgroundWorker = Depends(get_worker),
) -> dict:
    """Enqueue a report computation job. Returns job_id immediately."""
    job = repo.create()
    worker.submit(job.job_id, lambda: compute_report(body.label))
    return {"job_id": job.job_id}


@router.get("/{job_id}")
def get_report(
    job_id: str,
    repo: InMemoryJobRepository = Depends(get_repo),
) -> ReportJob:
    """Return job status and result (if completed)."""
    job = repo.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    result = ReportResult(**job.result) if job.result else None
    return ReportJob(
        job_id=job.job_id,
        status=job.status,
        result=result,
        error=job.error,
    )
