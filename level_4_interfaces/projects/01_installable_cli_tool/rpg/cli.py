# Typer CLI — five commands: new-game, play, simulate, report, status.
# This is the entry point registered in pyproject.toml [project.scripts].

import logging
from pathlib import Path
from typing import Annotated

import typer

from rpg.domain import HeroClass

logger = logging.getLogger(__name__)

app = typer.Typer(
    name="rpg",
    help="RPG Dungeon — a terminal role-playing game.",
    no_args_is_help=True,
)

_ROOT = Path(__file__).parent.parent
LOGS_DIR = _ROOT / "logs"


def _setup() -> None:
    """Configure logging — called at the start of every command."""
    import os
    from rpg.logging_setup import setup_logging, setup_log_files
    level = os.environ.get("RPG_LOG_LEVEL", "INFO")
    try:
        setup_logging(level)
        setup_log_files(LOGS_DIR)
    except NotImplementedError:
        pass  # student hasn't implemented logging yet — continue without it


@app.command("new-game")
def new_game(
    name: Annotated[str, typer.Option("--name", help="Hero name")] = "Hero",
    hero_class: Annotated[HeroClass, typer.Option("--class", "--hero-class",
                help="Hero class")] = HeroClass.warrior,
) -> None:
    """Create a new hero and save it."""
    _setup()
    # TODO:
    # 1. from rpg.game import make_hero, save_current_hero
    # 2. hero = make_hero(name, hero_class)
    # 3. save_current_hero(hero)
    # 4. typer.echo(f"New game started: {name} the {hero_class.value}")
    raise NotImplementedError


@app.command()
def play() -> None:
    """Start the interactive game loop."""
    _setup()
    # TODO:
    # 1. from rpg.game import load_current_hero, save_current_hero, load_monsters, run_combat
    # 2. Load hero (if None, prompt name+class and create one)
    # 3. Load monsters
    # 4. Main loop: show stats, [f]ight / [s]ave / [q]uit
    # 5. On quit: generate_reports(session) and show paths
    raise NotImplementedError


@app.command()
def simulate(
    battles: Annotated[int, typer.Option("--battles", help="Number of battles")] = 5,
) -> None:
    """Auto-simulate N battles and generate a session report."""
    _setup()
    # TODO:
    # 1. from rpg.game import load_current_hero, load_monsters, simulate_battles, generate_reports, save_current_hero
    # 2. hero = load_current_hero(); if None: typer.echo("No save."); raise typer.Exit(1)
    # 3. monsters = load_monsters()
    # 4. session = simulate_battles(hero, monsters, battles)
    # 5. save_current_hero(hero)
    # 6. json_path, md_path = generate_reports(session)
    # 7. typer.echo(f"Done. {session.wins}/{battles} wins. Gold: {session.gold_earned}")
    # 8. typer.echo(f"Reports: {json_path}, {md_path}")
    raise NotImplementedError


@app.command()
def report() -> None:
    """Show the most recent session report."""
    _setup()
    # TODO:
    # 1. from rpg.game import REPORTS_DIR
    # 2. Find the most recently modified *.md file in REPORTS_DIR
    # 3. If none found: typer.echo("No reports found."); return
    # 4. typer.echo(path.read_text())
    raise NotImplementedError


@app.command()
def status() -> None:
    """Show current save file info."""
    _setup()
    # TODO:
    # 1. from rpg.game import load_current_hero
    # 2. hero = load_current_hero(); if None: typer.echo("No save found."); return
    # 3. from rpg.output import show_hero_stats
    # 4. try: show_hero_stats(hero) except NotImplementedError: typer.echo(f"{hero.name} ...")
    raise NotImplementedError


def main() -> None:
    """Entry point registered in pyproject.toml [project.scripts]."""
    app()


if __name__ == "__main__":
    main()
