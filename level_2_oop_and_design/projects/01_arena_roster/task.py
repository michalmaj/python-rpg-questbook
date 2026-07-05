"""Project 01: Arena Roster

Build a small roster of characters for an arena.

Your task: implement the three classes and two functions below.
Run `uv run python check.py` from this folder to verify your work.
"""


class Character:
    """Base class for all arena combatants."""

    def __init__(self, name: str, hp: int, max_hp: int, atk: int, def_: int) -> None:
        raise NotImplementedError

    def take_damage(self, amount: int) -> None:
        """Reduce HP by amount. HP cannot go below 0."""
        raise NotImplementedError

    @property
    def is_alive(self) -> bool:
        """Return True if HP > 0."""
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Hero(Character):
    """A player-controlled hero."""

    def __init__(
        self,
        name: str,
        hp: int,
        max_hp: int,
        atk: int,
        def_: int,
        hero_class: str,
        potions: int,
    ) -> None:
        raise NotImplementedError


class Monster(Character):
    """An enemy combatant."""

    def __init__(
        self,
        name: str,
        hp: int,
        max_hp: int,
        atk: int,
        def_: int,
        reward_gold: int,
    ) -> None:
        raise NotImplementedError


def build_roster() -> list[Character]:
    """Return a list of at least 3 characters (mix of Hero and Monster).

    Example:
        [Hero("Ada", ...), Hero("Rex", ...), Monster("Goblin", ...)]
    """
    raise NotImplementedError


def print_roster(roster: list[Character]) -> None:
    """Print each character's name, type, and current HP.

    Example output:
        [Hero]    Ada      HP: 120/120
        [Monster] Goblin   HP: 30/30
    """
    raise NotImplementedError
