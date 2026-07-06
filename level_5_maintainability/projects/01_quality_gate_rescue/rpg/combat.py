# combat.py — BEFORE quality gate rescue
# Fix the type issues and style violations in this file.

from typing import Any

from rpg.domain import Hero, Monster


def compute_damage(attacker: Any, defender: Any) -> int:  # Any should be Hero | Monster
    raw = attacker.atk - defender.atk // 2
    return max(raw, 1)


def run_combat(hero: Hero, monster: Monster) -> str:
    round_num = 0
    while hero.is_alive() and monster.is_alive():
        round_num += 1
        dmg = compute_damage(hero, monster)
        monster.take_damage(dmg)
        if not monster.is_alive():
            break
        hero.take_damage(compute_damage(monster, hero))

    if hero.is_alive():
        return f"{hero.name} wins after {round_num} rounds"
    return f"{monster.name} wins after {round_num} rounds"
