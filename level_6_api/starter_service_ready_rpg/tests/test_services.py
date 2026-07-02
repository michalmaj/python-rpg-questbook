# level_6_api/starter_service_ready_rpg/tests/test_services.py
from unittest.mock import MagicMock

import pytest

from rpg.domain import BattleResult, Hero, HeroClass, Monster
from rpg.services import BattleService, create_hero


def _goblin() -> Monster:
    return Monster(name="Goblin", hp=30, atk=8, def_=2, gold=10)


def _mock_service(monster: Monster | None = None) -> BattleService:
    repo = MagicMock()
    repo.get.return_value = monster or _goblin()
    repo.list_all.return_value = [_goblin()]
    return BattleService(monster_repo=repo)


def test_simulate_returns_battle_result() -> None:
    svc = _mock_service()
    hero = create_hero("Ada", HeroClass.warrior)
    result = svc.simulate(hero, "Goblin")
    assert isinstance(result, BattleResult)
    assert result.winner in ("hero", "monster")
    assert result.rounds >= 1


def test_simulate_raises_for_unknown_monster() -> None:
    repo = MagicMock()
    repo.get.return_value = None
    svc = BattleService(monster_repo=repo)
    hero = create_hero("Ada", HeroClass.warrior)
    with pytest.raises(ValueError, match="not found"):
        svc.simulate(hero, "unknown")


def test_get_available_monsters() -> None:
    svc = _mock_service()
    monsters = svc.get_available_monsters()
    assert len(monsters) == 1
    assert monsters[0].name == "Goblin"


def test_get_hero_classes() -> None:
    svc = _mock_service()
    classes = svc.get_hero_classes()
    assert "warrior" in classes
    assert "mage" in classes
    assert "rogue" in classes


def test_create_hero_warrior() -> None:
    hero = create_hero("Ada", HeroClass.warrior)
    assert hero.hp == 120
    assert hero.atk == 12
    assert hero.def_ == 6
