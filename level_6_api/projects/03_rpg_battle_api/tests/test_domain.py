# level_6_api/starter_service_ready_rpg/tests/test_domain.py
from rpg.domain import BattleResult, Hero, HeroClass, Monster


def test_monster_take_damage() -> None:
    m = Monster(name="Goblin", hp=30, atk=8, def_=2, gold=10)
    m.take_damage(10)
    assert m.hp == 20


def test_monster_cannot_go_below_zero() -> None:
    m = Monster(name="Goblin", hp=30, atk=8, def_=2, gold=10)
    m.take_damage(100)
    assert m.hp == 0


def test_monster_is_alive() -> None:
    m = Monster(name="Goblin", hp=30, atk=8, def_=2, gold=10)
    assert m.is_alive is True
    m.take_damage(30)
    assert m.is_alive is False


def test_hero_class_values() -> None:
    assert HeroClass.warrior == "warrior"
    assert HeroClass.mage == "mage"
    assert HeroClass.rogue == "rogue"


def test_battle_result_fields() -> None:
    r = BattleResult(
        hero_name="Ada", monster_name="Goblin",
        winner="hero", rounds=3, gold_earned=10,
    )
    assert r.winner == "hero"
    assert r.gold_earned == 10
