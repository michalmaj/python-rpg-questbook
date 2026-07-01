"""test_combat.py — complete from M05; add tests for uncovered branches."""
import pytest
from rpg import Hero, HeroClass, Monster, compute_damage, simulate_turn


def test_compute_damage_normal() -> None:
    assert compute_damage(10, 5, 3) == 8


def test_compute_damage_minimum() -> None:
    assert compute_damage(5, 10, 1) == 1


@pytest.mark.parametrize("atk,def_,roll,expected", [
    (10, 5, 3, 8),
    (5, 10, 1, 1),
    (20, 0, 6, 26),
], ids=["normal", "min_damage", "max_hit"])
def test_compute_damage_parametrized(atk: int, def_: int, roll: int, expected: int) -> None:
    assert compute_damage(atk, def_, roll) == expected


def test_hero_take_damage(warrior: Hero) -> None:
    warrior.take_damage(20)
    assert warrior.hp == 100


def test_hero_take_damage_cannot_go_negative(warrior: Hero) -> None:
    warrior.take_damage(999)
    assert warrior.hp == 0


def test_hero_is_alive_true(warrior: Hero) -> None:
    assert warrior.is_alive is True


def test_hero_is_alive_false(make_hero: object) -> None:
    hero = make_hero(hp=0)  # type: ignore[call-arg]
    assert hero.is_alive is False  # type: ignore[union-attr]


def test_use_potion_heals(warrior: Hero) -> None:
    warrior.hp = 90
    used = warrior.use_potion()
    assert used is True
    assert warrior.hp == 120


def test_use_potion_empty(make_hero: object) -> None:
    hero = make_hero(potions=0)  # type: ignore[call-arg]
    assert hero.use_potion() is False  # type: ignore[union-attr]


@pytest.mark.parametrize("hero_roll,monster_roll,expect_hero_alive,expect_monster_alive", [
    (6, 1, True, False),   # hero one-shots goblin
    (1, 6, False, True),   # goblin one-shots hero (use a weak hero)
], ids=["hero_wins", "monster_wins"])
def test_simulate_turn(
    hero_roll: int, monster_roll: int, expect_hero_alive: bool, expect_monster_alive: bool,
) -> None:
    if not expect_hero_alive:
        hero = Hero(name="Weak", hero_class=HeroClass.warrior, hp=1, max_hp=1, atk=1, def_=0)
        monster = Monster(name="Strong", hp=100, atk=100, def_=0, gold=0)
    else:
        hero = Hero(name="Strong", hero_class=HeroClass.warrior, hp=100, max_hp=100, atk=100, def_=0)
        monster = Monster(name="Weak", hp=1, atk=1, def_=0, gold=10)
    alive_h, alive_m = simulate_turn(hero, monster, hero_roll, monster_roll)
    assert alive_h is expect_hero_alive
    assert alive_m is expect_monster_alive
