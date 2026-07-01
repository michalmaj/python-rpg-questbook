# rpg/domain.py — pure domain models (no Pydantic)
# Copy Hero and HeroClass from your Level 2 work.
# Boundary models (SaveGameModel, CombatLogRow) live in rpg/schemas.py.

from dataclasses import dataclass
from enum import Enum


class HeroClass(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"


@dataclass
class Hero:
    name: str
    hero_class: HeroClass
    hp: int
    max_hp: int
    atk: int
    def_: int
    potions: int = 3
    gold: int = 0
    wins: int = 0
    losses: int = 0
