# Pure domain models — no Pydantic, no Typer, no Rich.
# This file must stay clean of all interface concerns.

from dataclasses import dataclass
from enum import Enum


class HeroClass(str, Enum):
    warrior = "warrior"
    mage = "mage"
    rogue = "rogue"


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

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def use_potion(self) -> bool:
        if self.potions <= 0:
            return False
        self.hp = min(self.hp + 30, self.max_hp)
        self.potions -= 1
        return True


@dataclass
class Monster:
    name: str
    hp: int
    atk: int
    def_: int
    gold: int

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)
