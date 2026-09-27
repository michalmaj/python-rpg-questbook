import copy
import random

from .domain import BattleResult, Hero, HeroClass, Monster, TournamentSummary
from .repositories import MonsterRepository

HERO_CLASS_STATS: dict[HeroClass, dict[str, int]] = {
    HeroClass.warrior: {"hp": 120, "atk": 12, "def_": 6},
    HeroClass.mage: {"hp": 80, "atk": 18, "def_": 2},
    HeroClass.rogue: {"hp": 100, "atk": 15, "def_": 4},
}


def create_hero(name: str, hero_class: HeroClass) -> Hero:
    stats = HERO_CLASS_STATS[hero_class]
    return Hero(
        name=name,
        hero_class=hero_class,
        hp=stats["hp"],
        max_hp=stats["hp"],
        atk=stats["atk"],
        def_=stats["def_"],
    )


class BattleService:
    def __init__(self, monster_repo: MonsterRepository) -> None:
        self._repo = monster_repo

    def get_available_monsters(self) -> list[Monster]:
        return self._repo.list_all()

    def get_hero_classes(self) -> list[str]:
        return [hc.value for hc in HeroClass]

    def simulate(self, hero: Hero, monster_name: str) -> BattleResult:
        monster = self._repo.get(monster_name)
        if monster is None:
            raise ValueError(f"Monster '{monster_name}' not found")
        monster = copy.deepcopy(monster)
        h = copy.deepcopy(hero)
        rounds = 0
        while h.hp > 0 and monster.hp > 0:
            rounds += 1
            monster.take_damage(max(1, h.atk + random.randint(1, 6) - monster.def_))
            if not monster.is_alive:
                return BattleResult(
                    hero_name=h.name,
                    monster_name=monster.name,
                    winner="hero",
                    rounds=rounds,
                    gold_earned=monster.gold,
                )
            h.hp = max(0, h.hp - max(1, monster.atk + random.randint(1, 6) - h.def_))
        return BattleResult(
            hero_name=h.name,
            monster_name=monster.name,
            winner="monster",
            rounds=rounds,
            gold_earned=0,
        )


def _fight(hero: Hero, monster: Monster) -> BattleResult:
    """Pure battle function — module-level so ProcessPoolExecutor can pickle it."""
    h, m = copy.deepcopy(hero), copy.deepcopy(monster)
    rounds = 0
    while h.hp > 0 and m.hp > 0:
        rounds += 1
        m.take_damage(max(1, h.atk + random.randint(1, 6) - m.def_))
        if not m.is_alive:
            return BattleResult(hero_name=h.name, monster_name=m.name,
                                winner="hero", rounds=rounds, gold_earned=m.gold)
        h.hp = max(0, h.hp - max(1, m.atk + random.randint(1, 6) - h.def_))
    return BattleResult(hero_name=h.name, monster_name=m.name,
                        winner="monster", rounds=rounds, gold_earned=0)


# Monster combat stats mirroring data/monsters.json.
# Kept here (not loaded from disk) so _simulate_one is fully self-contained
# and picklable by ProcessPoolExecutor worker processes.
_WORKER_MONSTERS = [
    {"hp": 30,  "atk": 8,  "def_": 2},  # Goblin
    {"hp": 60,  "atk": 12, "def_": 4},  # Orc
    {"hp": 150, "atk": 20, "def_": 8},  # Dragon
]


def _simulate_one(seed: int) -> dict:
    """Simulate one battle deterministically from seed.

    Module-level so ProcessPoolExecutor can pickle it. Uses HERO_CLASS_STATS
    and _WORKER_MONSTERS from this module — single source of truth for stats.
    The entire battle uses one seeded RNG so the result is reproducible.
    Returns {"winner": "hero" | "monster", "rounds": int}.
    """
    rng = random.Random(seed)
    hero_class = rng.choice(list(HeroClass))
    stats = HERO_CLASS_STATS[hero_class]
    hero_hp, hero_atk, hero_def = stats["hp"], stats["atk"], stats["def_"]
    m = dict(rng.choice(_WORKER_MONSTERS))
    rounds = 0
    while hero_hp > 0 and m["hp"] > 0:
        rounds += 1
        m["hp"] = max(0, m["hp"] - max(1, hero_atk + rng.randint(1, 6) - m["def_"]))
        if m["hp"] <= 0:
            return {"winner": "hero", "rounds": rounds}
        hero_hp = max(0, hero_hp - max(1, m["atk"] + rng.randint(1, 6) - hero_def))
    return {"winner": "monster", "rounds": rounds}


class SimulationService:
    def __init__(self, monster_repo: MonsterRepository) -> None:
        self._repo = monster_repo

    def simulate_tournament(self, n: int) -> TournamentSummary:
        """Simulate n random battles. Blocks the calling thread until done."""
        monsters = self._repo.list_all()
        hero_wins = 0
        for _ in range(n):
            hero_class = random.choice(list(HeroClass))
            hero = create_hero("Hero", hero_class)
            monster = copy.deepcopy(random.choice(monsters))
            result = _fight(hero, monster)
            if result.winner == "hero":
                hero_wins += 1
        return TournamentSummary(
            total_battles=n, hero_wins=hero_wins, monster_wins=n - hero_wins
        )
