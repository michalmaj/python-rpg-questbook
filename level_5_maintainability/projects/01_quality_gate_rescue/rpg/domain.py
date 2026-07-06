# domain.py — BEFORE quality gate rescue
# This file has intentional problems. Fix them.
#
# Problems to fix:
#  1. Ruff: unused import (os), old-style List/Dict/Optional from typing
#  2. mypy/pyright: missing return type annotations, use of Any, wrong type
#  3. Line too long (>88 chars) on the combat function

import os  # noqa: F401 — remove this line, os is not used
from typing import Any, Dict, List, Optional


class HeroClass:
    WARRIOR = "warrior"
    MAGE = "mage"
    RANGER = "ranger"


class Hero:
    def __init__(self, name: str, hero_class: str, hp: int, atk: int):
        self.name = name
        self.hero_class = hero_class
        self.hp = hp
        self.atk = atk

    def is_alive(self):  # missing return type annotation
        return self.hp > 0

    def take_damage(self, amount: int):  # missing return type annotation
        self.hp = max(self.hp - amount, 0)


class Monster:
    def __init__(self, name: str, hp: int, atk: int, gold: int):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.gold = gold

    def is_alive(self):  # missing return type annotation
        return self.hp > 0

    def take_damage(self, amount: int):  # missing return type annotation
        self.hp = max(self.hp - amount, 0)


def build_roster() -> List[Any]:  # List[Any] should be list[Hero | Monster]
    return [
        Hero("Ada", HeroClass.WARRIOR, 120, 15),
        Hero("Zara", HeroClass.MAGE, 80, 22),
        Monster("Goblin", 30, 8, 5),
        Monster("Dragon", 200, 30, 100),
    ]


def get_hero(roster: List[Any], name: str) -> Optional[Hero]:  # old-style Optional
    for character in roster:
        if isinstance(character, Hero) and character.name.lower() == name.lower():
            return character
    return None


def get_monster(roster: List[Any], name: str) -> Optional[Monster]:  # old-style Optional
    for character in roster:
        if isinstance(character, Monster) and character.name.lower() == name.lower():
            return character
    return None


def summarise_roster(roster: List[Any]) -> Dict[str, int]:  # old-style Dict
    return {"heroes": sum(1 for c in roster if isinstance(c, Hero)), "monsters": sum(1 for c in roster if isinstance(c, Monster))}  # line too long
