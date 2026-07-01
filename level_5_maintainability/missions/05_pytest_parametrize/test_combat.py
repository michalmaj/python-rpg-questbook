"""test_combat.py — extend with parametrize decorators."""
import pytest
from rpg import Hero, HeroClass, Monster, compute_damage, simulate_turn


# Pre-provided: 4 plain tests from M04 solution
def test_compute_damage_normal() -> None:
    assert compute_damage(10, 5, 3) == 8


def test_compute_damage_minimum() -> None:
    assert compute_damage(5, 10, 1) == 1


def test_hero_take_damage(warrior: Hero) -> None:
    warrior.take_damage(20)
    assert warrior.hp == 100


def test_use_potion_empty(make_hero: object) -> None:
    hero = make_hero(potions=0)  # type: ignore[call-arg]
    assert hero.use_potion() is False


# TODO 1: Parametrize compute_damage to cover normal, minimum, and maximum cases
#
# @pytest.mark.parametrize("atk,def_,roll,expected", [
#     (10, 5, 3, 8),    # normal hit
#     (5, 10, 1, 1),    # minimum — never 0
#     (20, 0, 6, 26),   # maximum hit
# ], ids=["normal", "min_damage", "max_hit"])
# def test_compute_damage_parametrized(atk: int, def_: int, roll: int, expected: int) -> None:
#     assert compute_damage(atk, def_, roll) == expected


# TODO 2: Parametrize simulate_turn to cover "hero wins", "hero loses", "both survive"
#
# Hint: create heroes/monsters with specific stats to control outcomes.
# Use simulate_turn(hero, monster, hero_roll=6, monster_roll=1) etc.
