# Rich output functions — all user-facing terminal output goes through here.
# Port from M05.

from rich.console import Console
from rich.panel import Panel  # noqa: F401
from rich.table import Table  # noqa: F401
from rich.text import Text  # noqa: F401

from rpg.domain import Hero, Monster

console = Console()


def show_hero_stats(hero: Hero) -> None:
    # TODO: display hero stats as a Table (name, class, HP, gold, potions, W/L)
    raise NotImplementedError


def show_combat_start(hero: Hero, monster: Monster) -> None:
    # TODO: display a Panel announcing the battle
    raise NotImplementedError


def show_combat_result(winner: str, gold_gained: int = 0) -> None:
    # TODO: Panel with green border for win, red for loss
    raise NotImplementedError


def show_error(message: str) -> None:
    # TODO: console.print(message, style="bold red", stderr=True)
    raise NotImplementedError
