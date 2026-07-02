"""Run this to see the RPG service in action before starting the API missions."""
from pathlib import Path

from rpg.domain import HeroClass
from rpg.repositories import MonsterRepository
from rpg.services import BattleService, create_hero

_DATA = Path(__file__).parent / "data"


def main() -> None:
    service = BattleService(monster_repo=MonsterRepository(_DATA / "monsters.json"))
    monsters = service.get_available_monsters()
    print(f"Monsters: {[m.name for m in monsters]}")
    hero = create_hero("Ada", HeroClass.warrior)
    result = service.simulate(hero, "Goblin")
    print(f"{result.hero_name} vs {result.monster_name} → {result.winner} ({result.rounds} rounds)")


if __name__ == "__main__":
    main()
