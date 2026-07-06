"""Project 01: Quest Master CLI

Build a three-command Typer CLI for your RPG.
All data is hardcoded — focus on CLI design, not file I/O.

Your task: implement the three subcommands below.
Run `uv run python task.py --help` to test the CLI.
Run `uv run python check.py` to verify your work.
"""

from __future__ import annotations

import typer

# ── Hardcoded data ────────────────────────────────────────────────────────────

HEROES: dict[str, dict] = {
    "ada":  {"name": "Ada",  "hero_class": "warrior", "hp": 120},
    "zara": {"name": "Zara", "hero_class": "mage",    "hp": 80},
    "rex":  {"name": "Rex",  "hero_class": "ranger",  "hp": 100},
}

MONSTERS: dict[str, dict] = {
    "goblin": {"name": "Goblin", "hp": 30},
    "orc":    {"name": "Orc",    "hp": 60},
    "dragon": {"name": "Dragon", "hp": 200},
}

# ── Typer app ─────────────────────────────────────────────────────────────────

app = typer.Typer(help="Quest Master — your RPG command center.")


@app.command()
def hero(
    name: str = typer.Option(..., "--name", "-n", help="Hero name (Ada, Zara, Rex)"),
    hero_class: str = typer.Option("", "--class", "-c", help="Filter by class"),
) -> None:
    """Show a hero's stats card."""
    raise NotImplementedError


@app.command()
def monsters() -> None:
    """List all available monsters."""
    raise NotImplementedError


@app.command()
def battle(
    hero_name: str = typer.Option(..., "--hero", help="Hero name"),
    monster_name: str = typer.Option(..., "--monster", help="Monster name"),
) -> None:
    """Simulate a battle between a hero and a monster.

    Unknown names must print a friendly error message and exit with code 1.
    Do NOT let Python raise an unhandled exception.
    """
    raise NotImplementedError


if __name__ == "__main__":
    app()
