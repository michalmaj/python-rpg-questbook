"""CLI for the Concurrent Tournament Runner."""
import time
import typer
from api.dependencies import get_job_repo, get_simulation_service, get_worker
from jobs.jobs import JobStatus

app = typer.Typer()


@app.command()
def start(battles: int = typer.Option(1000, "--battles", "-n")) -> None:
    """Start a tournament in the background and print the job_id."""
    svc = get_simulation_service()
    repo = get_job_repo()
    worker = get_worker()
    import uuid
    job_id = str(uuid.uuid4())
    repo.create(job_id)
    worker.submit(job_id, lambda: svc.simulate_tournament(battles).to_dict())
    typer.echo(f"Tournament started: {job_id}")
    typer.echo("Check status: rpg status <job_id>")


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
    summary = TournamentSummary(**job.result)
    typer.echo(summary.to_markdown())


if __name__ == "__main__":
    app()
