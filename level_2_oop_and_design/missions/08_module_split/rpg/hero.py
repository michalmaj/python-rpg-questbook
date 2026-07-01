# rpg/hero.py — Hero class (already complete, provided for you)

from enum import Enum


class HeroClass(Enum):
    WARRIOR = "warrior"
    MAGE    = "mage"
    ROGUE   = "rogue"


class Hero:
    def __init__(
        self,
        name:       str,
        hero_class: HeroClass,
        hp:         int,
        max_hp:     int,
        atk:        int,
        def_:       int,
        potions:    int,
        gold:       int,
    ) -> None:
        self.name:       str       = name
        self.hero_class: HeroClass = hero_class
        self.hp:         int       = hp
        self.max_hp:     int       = max_hp
        self.atk:        int       = atk
        self.def_:       int       = def_
        self.potions:    int       = potions
        self.gold:       int       = gold

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def heal(self, amount: int) -> None:
        self.hp = min(self.hp + amount, self.max_hp)

    def __repr__(self) -> str:
        return f"Hero(name={self.name!r}, class={self.hero_class.value}, hp={self.hp}/{self.max_hp})"
