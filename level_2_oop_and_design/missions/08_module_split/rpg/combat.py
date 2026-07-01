# rpg/combat.py — damage calculation and combat resolution

import random

from rpg.hero import Hero
from rpg.monster import Monster


def roll(sides: int) -> int:
    return random.randint(1, sides)


def compute_damage(atk: int, def_: int) -> int:
    """Return damage dealt: base attack + d6 roll, minus defence. Minimum 1."""
    # TODO: implement this formula:
    #   damage = atk + roll(6) - def_
    #   return max(1, damage)
    ...


def hero_turn(hero: Hero, monster: Monster) -> tuple[int, bool]:
    """
    Resolve the hero's attack against the monster.
    Returns (damage_dealt, was_crit).
    A crit happens on a d20 roll of 20 — doubles the attack before computing damage.
    """
    # TODO: implement hero_turn.
    #
    # 1. Roll a d20. If the result is 20, it's a crit: use atk = hero.atk * 2.
    #    Otherwise use atk = hero.atk.
    # 2. Call compute_damage(atk, monster.def_) to get the damage.
    # 3. Call monster.take_damage(damage).
    # 4. Return (damage, is_crit).
    ...


def monster_turn(monster: Monster, hero: Hero) -> tuple[int, bool]:
    """
    Resolve the monster's attack against the hero.
    Returns (damage_dealt, was_crit).
    Same crit logic as hero_turn.
    """
    # TODO: implement monster_turn.
    #   Same structure as hero_turn, but attacker = monster and target = hero.
    ...
