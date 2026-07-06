"""Project 02: Observable Battle Runner

Extend Quest Master CLI with structured logging.
Every battle writes events to two log files: app.log and combat.log.

Your task: implement the logging setup and the battle command.
Run `uv run python task.py battle --hero Ada --monster Goblin` to test.
Run `uv run python check.py` to verify your work.
"""

from __future__ import annotations

import logging
from pathlib import Path

import typer

# ── Log file paths ────────────────────────────────────────────────────────────

APP_LOG = Path("app.log")
COMBAT_LOG = Path("combat.log")

# ── Hardcoded data ────────────────────────────────────────────────────────────

HEROES: dict[str, dict] = {
    "ada":  {"name": "Ada",  "hero_class": "warrior", "hp": 120, "atk": 15},
    "zara": {"name": "Zara", "hero_class": "mage",    "hp": 80,  "atk": 22},
    "rex":  {"name": "Rex",  "hero_class": "ranger",  "hp": 100, "atk": 18},
}

MONSTERS: dict[str, dict] = {
    "goblin": {"name": "Goblin", "hp": 30,  "atk": 8},
    "orc":    {"name": "Orc",    "hp": 60,  "atk": 12},
    "dragon": {"name": "Dragon", "hp": 200, "atk": 30},
}

# ── Loggers ───────────────────────────────────────────────────────────────────

logger = logging.getLogger("rpg")
combat_logger = logging.getLogger("rpg.combat")


def setup_logging() -> None:
    """Configure two FileHandlers:

    - app.log:    receives INFO+ from the "rpg" logger
    - combat.log: receives DEBUG+ from the "rpg.combat" logger

    Do NOT log to stdout/stderr — use typer.echo() for user-facing messages.
    """
    raise NotImplementedError


# ── Typer app ─────────────────────────────────────────────────────────────────

app = typer.Typer(help="Observable Battle Runner — battles with structured logging.")


@app.command()
def battle(
    hero_name: str = typer.Option(..., "--hero", help="Hero name"),
    monster_name: str = typer.Option(..., "--monster", help="Monster name"),
) -> None:
    """Simulate a battle and log every round to combat.log.

    Requirements:
    - Call setup_logging() before anything else.
    - Unknown hero or monster: typer.echo(message, err=True) + raise typer.Exit(1).
      Log the error to app.log via logger.error() or logger.exception().
      Do NOT print a Python traceback to the terminal.
    - Each combat round: log to combat_logger (e.g. "Round 1: Ada deals 15 damage")
    - Battle result: log to logger (e.g. "Ada defeated Goblin in 3 rounds")
    """
    raise NotImplementedError


if __name__ == "__main__":
    app()
