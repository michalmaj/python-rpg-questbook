import copy
import random

from .domain import BattleResult, Hero, HeroClass, Monster
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
