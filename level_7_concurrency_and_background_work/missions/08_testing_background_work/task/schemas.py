from pydantic import BaseModel, Field


class TournamentRequest(BaseModel):
    battles: int = Field(gt=0, le=1_000_000)


class JobStarted(BaseModel):
    job_id: str
    status: str = "pending"


class JobOut(BaseModel):
    job_id: str
    status: str
    result: dict | None = None
    error: str | None = None
