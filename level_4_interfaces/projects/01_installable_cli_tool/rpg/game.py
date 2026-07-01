# Core game logic — load catalogs, run combat, simulate battles.
# No Typer, no Rich, no argparse here.

import json  # noqa: F401
import logging
import random  # noqa: F401
from pathlib import Path

from pydantic import ValidationError  # noqa: F401

from rpg.domain import Hero, HeroClass, Monster
from rpg.schemas import SessionSummary, load_hero, save_hero

logger = logging.getLogger(__name__)
combat_logger = logging.getLogger("rpg.combat")

_ROOT = Path(__file__).parent.parent
DATA_DIR = _ROOT / "data"
SAVES_DIR = _ROOT / "saves"
SAVE_FILE = SAVES_DIR / "save_game.json"
REPORTS_DIR = _ROOT / "reports"


# ----- data loading -----------------------------------------------------------


def load_monsters() -> list[Monster]:
    """Load and validate monsters from data/monsters.json."""
    # TODO:
    # Open DATA_DIR / "monsters.json", validate each entry with MonsterConfig
    # (copy MonsterConfig from starter_verbose_rpg or reuse L3 pattern),
    # skip invalid entries with logger.warning(), return list[Monster]
    raise NotImplementedError


def load_hero_classes() -> dict:
    """Load hero class templates from data/hero_classes.json."""
    # TODO: open DATA_DIR / "hero_classes.json" and return parsed dict
    raise NotImplementedError


# ----- persistence helpers ---------------------------------------------------


def get_save_path() -> Path:
    return SAVE_FILE


def load_current_hero() -> Hero | None:
    return load_hero(SAVE_FILE)


def save_current_hero(hero: Hero) -> None:
    save_hero(hero, SAVE_FILE)
    logger.info("Saved hero: %s", hero.name)


# ----- pure logic -------------------------------------------------------------


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return max(1, atk + dice_roll - def_)


def make_hero(name: str, hero_class: HeroClass) -> Hero:
    """Create a fresh hero from templates."""
    # TODO: load_hero_classes(), pick the right entry, return Hero(...)
    raise NotImplementedError


# ----- combat -----------------------------------------------------------------


def run_combat(hero: Hero, monster: Monster) -> bool:
    """
    Run one interactive combat turn-by-turn.
    Import output functions locally to avoid circular imports.
    Returns True if hero wins.
    """
    # TODO: Port from starter_verbose_rpg/main.py.
    # Use output.show_combat_start, output.show_combat_result for user-facing output.
    # Use combat_logger.info/debug for logging.
    # Use input() for "Action — [a]ttack / [p]otion".
    raise NotImplementedError


def simulate_battles(hero: Hero, monsters: list[Monster], battles: int) -> SessionSummary:
    """
    Auto-simulate N battles (no input). Return a SessionSummary.
    """
    # TODO:
    # Record started_at = datetime.now()
    # For each battle: pick random monster, run simplified auto-combat (no input())
    # Accumulate wins, losses, gold
    # Return SessionSummary(started_at=..., hero_name=..., ...)
    raise NotImplementedError


# ----- reports ---------------------------------------------------------------


def generate_reports(session: SessionSummary) -> tuple[Path, Path]:
    """Write session_*.json and session_*.md to REPORTS_DIR. Return both paths."""
    # TODO: Port generate_reports() from M06.
    raise NotImplementedError
