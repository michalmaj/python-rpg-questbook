import typer
from api.dependencies import get_simulation_service

app = typer.Typer()


@app.command()
def simulate(battles: int = typer.Option(100, "--battles", "-n")) -> None:
    """Simulate a tournament (blocks until done)."""
    svc = get_simulation_service()
    typer.echo(f"Simulating {battles} battles...")
    summary = svc.simulate_tournament(battles)
    typer.echo(summary.to_markdown())


if __name__ == "__main__":
    app()
