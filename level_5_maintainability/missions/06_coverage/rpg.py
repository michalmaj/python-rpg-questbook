"""Pure domain functions for the RPG — no I/O, no CLI, no external libraries.

These are the functions worth testing first:
  - compute_damage: deterministic given atk, def_, roll
  - simulate_turn: one combat turn, modifies Hero and Monster in place
  - apply_potion: heals hero if potions remain
"""
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


def compute_damage(atk: int, def_: int, roll: int) -> int:
    """Damage dealt: max(1, atk + roll - def_). Minimum damage is always 1."""
    return max(1, atk + roll - def_)


def simulate_turn(
    hero: Hero, monster: Monster, hero_roll: int, monster_roll: int
) -> tuple[bool, bool]:
    """Simulate one full combat turn.

    Returns (hero_alive, monster_alive) after both attacks.
    Hero attacks first; if monster dies, monster's counterattack does not happen.
    """
    hero_dmg = compute_damage(hero.atk, monster.def_, hero_roll)
    monster.take_damage(hero_dmg)
    if not monster.is_alive:
        hero.gold += monster.gold
        hero.wins += 1
        return True, False
    monster_dmg = compute_damage(monster.atk, hero.def_, monster_roll)
    hero.take_damage(monster_dmg)
    if not hero.is_alive:
        hero.losses += 1
        return False, True
    return True, True
