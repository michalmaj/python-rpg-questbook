"""Pydantic schemas for the Background Report Queue API."""

from pydantic import BaseModel


class ReportRequest(BaseModel):
    """Request body for POST /reports."""
    label: str = "combat_report"


class ReportResult(BaseModel):
    """Computed report data stored as the job result."""
    total_sessions: int
    hero_wins: int
    monster_wins: int
    hero_win_rate: float
    avg_damage_dealt: float
    avg_damage_taken: float
    markdown: str


class ReportJob(BaseModel):
    """Job status returned by GET /reports/{job_id}."""
    job_id: str
    status: str           # "pending" | "running" | "completed" | "failed"
    result: ReportResult | None = None
    error: str | None = None
