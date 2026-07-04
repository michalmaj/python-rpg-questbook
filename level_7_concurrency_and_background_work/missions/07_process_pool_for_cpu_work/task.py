"""Mission 07: Process Pool for CPU-Bound Work.

Goal:  Use ProcessPoolExecutor to run battle simulations in parallel.
       CPU-bound work (pure computation) benefits from multiple processes.
Check: uv run python check.py
"""
import copy
import random
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from enum import StrEnum


class HeroClass(StrEnum):
    warrior = "warrior"
    mage = "mage"
    rogue = "rogue"


@dataclass
class Monster:
    name: str
    hp: int
    atk: int
    def_: int
    gold: int

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0


_MONSTERS = [
    {"name": "Goblin", "hp": 30, "atk": 8, "def_": 2, "gold": 10},
    {"name": "Orc", "hp": 60, "atk": 12, "def_": 4, "gold": 25},
    {"name": "Dragon", "hp": 150, "atk": 20, "def_": 8, "gold": 100},
]

_HERO_STATS = {
    "warrior": {"hp": 120, "atk": 12, "def_": 6},
    "mage": {"hp": 80, "atk": 18, "def_": 2},
    "rogue": {"hp": 100, "atk": 15, "def_": 4},
}


def _simulate_one(seed: int) -> dict:
    """Simulate one random battle. Module-level so ProcessPoolExecutor can pickle it.
    Returns {"winner": "hero" | "monster", "rounds": int}.
    """
    rng = random.Random(seed)
    hero_class = rng.choice(list(_HERO_STATS.keys()))
    stats = _HERO_STATS[hero_class]
    hero_hp, hero_atk, hero_def = stats["hp"], stats["atk"], stats["def_"]
    monster_data = rng.choice(_MONSTERS)
    m = Monster(**monster_data)
    rounds = 0
    while hero_hp > 0 and m.is_alive:
        rounds += 1
        m.take_damage(max(1, hero_atk + rng.randint(1, 6) - m.def_))
        if not m.is_alive:
            return {"winner": "hero", "rounds": rounds}
        hero_hp = max(0, hero_hp - max(1, m.atk + rng.randint(1, 6) - hero_def))
    return {"winner": "monster", "rounds": rounds}


def simulate_tournament_sequential(n: int) -> dict:
    """Simulate n battles sequentially (baseline for comparison)."""
    results = [_simulate_one(i) for i in range(n)]
    hero_wins = sum(1 for r in results if r["winner"] == "hero")
    return {"total_battles": n, "hero_wins": hero_wins, "monster_wins": n - hero_wins}


def simulate_tournament_parallel(n: int, workers: int = 4) -> dict:
    """TODO: Use ProcessPoolExecutor to simulate n battles in parallel.
    Use pool.map(_simulate_one, range(n)) with max_workers=workers.
    Return same dict format as simulate_tournament_sequential.
    """
    raise NotImplementedError
