"""Combat engine for the RPG arena.

This module is production code — do NOT modify it.
Your job is to write tests in tests/test_combat.py that verify its behaviour.
One test will find a hidden bug; mark that test with @pytest.mark.xfail.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Fighter:
    name: str
    hp: int
    atk: int
    def_: int


def compute_damage(atk: int, bonus: int, def_: int) -> int:
    """Return the damage dealt after applying bonus and defence.

    Formula: max(atk + bonus - def_, 1)

    NOTE: There is a bug in this implementation.
          A thorough test suite will detect it.
    """
    # BUG: should be max(..., 1) but uses max(..., 0)
    return max(atk + bonus - def_, 0)


def apply_damage(fighter: Fighter, damage: int) -> Fighter:
    """Return a new Fighter with HP reduced by damage (minimum 0)."""
    return Fighter(
        name=fighter.name,
        hp=max(fighter.hp - damage, 0),
        atk=fighter.atk,
        def_=fighter.def_,
    )


def run_combat(hero: Fighter, monster: Fighter) -> tuple[str, int]:
    """Simulate combat until one fighter reaches 0 HP.

    Returns:
        (winner_name, rounds_taken)
    """
    if hero.hp <= 0 or monster.hp <= 0:
        raise ValueError("Both fighters must start with HP > 0")

    h, m = hero, monster
    rounds = 0
    while h.hp > 0 and m.hp > 0:
        rounds += 1
        dmg = compute_damage(h.atk, 0, m.def_)
        m = apply_damage(m, dmg)
        if m.hp <= 0:
            break
        dmg = compute_damage(m.atk, 0, h.def_)
        h = apply_damage(h, dmg)

    winner = h.name if h.hp > 0 else m.name
    return winner, rounds


def compute_gold_reward(base_gold: int, bonus_pct: int) -> int:
    """Return gold reward after applying bonus percentage.

    Args:
        base_gold: base gold value (must be >= 0)
        bonus_pct: percentage bonus (0-100)

    Raises:
        ValueError: if base_gold < 0 or bonus_pct not in 0..100
    """
    if base_gold < 0:
        raise ValueError(f"base_gold must be >= 0, got {base_gold}")
    if not (0 <= bonus_pct <= 100):
        raise ValueError(f"bonus_pct must be 0..100, got {bonus_pct}")
    return base_gold + base_gold * bonus_pct // 100
