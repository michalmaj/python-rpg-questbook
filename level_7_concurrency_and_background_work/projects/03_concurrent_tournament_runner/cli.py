"""CLI for the Concurrent Tournament Runner."""
import time
import uuid

import typer
from api.dependencies import get_job_repo, get_worker
from jobs.jobs import JobStatus

app = typer.Typer()


@app.command()
def start(battles: int = typer.Option(1000, "--battles", "-n")) -> None:
    """Run a tournament on the ProcessPool worker and print the result when done.

    The worker runs on a daemon thread (see BackgroundWorker/ProcessPoolTournamentWorker
    in jobs/jobs.py) — daemon threads are killed the moment their process exits. A
    short-lived CLI invocation has no way to outlive itself, so this command waits for
    the job to reach a terminal status before exiting. The job is still tracked through
    the same job_id/JobRepository pattern the API uses: `status`/`report` afterward read
    the same persisted, completed job from disk.
    """
    if battles <= 0:
        typer.echo("battles must be a positive integer", err=True)
        raise typer.Exit(1)

    repo = get_job_repo()
    worker = get_worker()
    job_id = str(uuid.uuid4())
    repo.create(job_id)
    worker.submit(job_id, battles)
    typer.echo(f"Tournament started: {job_id}")

    deadline = time.monotonic() + 120
    job = repo.get(job_id)
    while time.monotonic() < deadline:
        job = repo.get(job_id)
        if job.status in (JobStatus.completed, JobStatus.failed):
            break
        time.sleep(0.2)
    else:
        typer.echo(f"Tournament did not finish within 120s (job_id={job_id})", err=True)
        raise typer.Exit(1)

    if job.status == JobStatus.failed:
        typer.echo(f"Tournament failed: {job.error}", err=True)
        raise typer.Exit(1)
    typer.echo(f"Tournament completed: {job.result}")
    typer.echo(f"Check status: python cli.py status {job_id}")


@app.command()
def status(job_id: str) -> None:
    """Check the status of a tournament job."""
    repo = get_job_repo()
    job = repo.get(job_id)
    if job is None:
        typer.echo(f"Job '{job_id}' not found", err=True)
        raise typer.Exit(1)
    typer.echo(f"Status: {job.status}")
    if job.error:
        typer.echo(f"Error: {job.error}")


@app.command()
def report(job_id: str) -> None:
    """Print the Markdown report for a completed tournament."""
    from rpg.domain import TournamentSummary
    repo = get_job_repo()
    job = repo.get(job_id)
    if job is None:
        typer.echo(f"Job '{job_id}' not found", err=True)
        raise typer.Exit(1)
    if job.status != JobStatus.completed:
        typer.echo(f"Job not completed yet (status: {job.status})", err=True)
        raise typer.Exit(1)
    summary = TournamentSummary(
        total_battles=job.result["total_battles"],
        hero_wins=job.result["hero_wins"],
        monster_wins=job.result["monster_wins"],
    )
    typer.echo(summary.to_markdown())


if __name__ == "__main__":
    app()
