"""Project 02: Character Sheet Builder

Combine Enum, dataclasses, type hints, and properties into a
complete character sheet system.

Your task: implement the classes below.
Run `uv run python check.py` from this folder to verify your work.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class HeroClass(Enum):
    """The three hero archetypes available in the arena."""
    WARRIOR = "warrior"
    MAGE = "mage"
    RANGER = "ranger"


@dataclass
class Weapon:
    """A weapon equipped by a hero.

    Attributes:
        name: display name, e.g. "Iron Sword"
        damage: base attack damage (positive int)
        weight: equipment weight in kg
    """
    name: str
    damage: int
    weight: float


@dataclass
class Armor:
    """Armor worn by a hero.

    Attributes:
        name: display name, e.g. "Leather Vest"
        defense: damage reduction (positive int)
        weight: equipment weight in kg
    """
    name: str
    defense: int
    weight: float


@dataclass
class CharacterSheet:
    """A complete character sheet for an arena hero.

    Attributes:
        name: hero's name
        hero_class: one of HeroClass.WARRIOR / MAGE / RANGER
        hp: current hit points
        weapon: equipped weapon (None if unarmed)
        armor: equipped armor (None if unarmored)
    """
    name: str
    hero_class: HeroClass
    hp: int
    weapon: Weapon | None = None
    armor: Armor | None = None

    @property
    def total_weight(self) -> float:
        """Sum of weapon and armor weight. 0.0 if slot is empty."""
        raise NotImplementedError

    @property
    def power_score(self) -> int:
        """Combat power rating.

        Formula: weapon.damage + armor.defense - int(total_weight // 5)
        Use 0 for any missing slot (no weapon → 0 damage, no armor → 0 defense).
        Minimum value is 0.
        """
        raise NotImplementedError

    @property
    def is_encumbered(self) -> bool:
        """True when total_weight exceeds 20.0 kg."""
        raise NotImplementedError

    def summary(self) -> str:
        """Return a human-readable one-line summary of this character.

        Must include the hero's name and hero_class value somewhere in the string.

        Example:
            "Ada [WARRIOR] — HP: 120  Power: 18  Weight: 9.5 kg"
        """
        raise NotImplementedError
