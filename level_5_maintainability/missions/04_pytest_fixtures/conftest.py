"""conftest.py — define fixtures here.

Fixtures are functions that provide test data. pytest injects them
by name into your test functions. Define them with @pytest.fixture.
"""
import pytest
from rpg import Hero, HeroClass, Monster


# TODO 1: Define a 'warrior' fixture that returns a warrior Hero.
#   name="Ada", hero_class=HeroClass.warrior, hp=120, max_hp=120, atk=12, def_=5
#
# @pytest.fixture
# def warrior() -> Hero:
#     ...


# TODO 2: Define a 'goblin' fixture that returns a Monster.
#   name="Goblin", hp=30, atk=8, def_=2, gold=10
#
# @pytest.fixture
# def goblin() -> Monster:
#     ...


# TODO 3: Define a 'make_hero' factory fixture.
#   It should return a function that accepts keyword arguments
#   and returns a Hero with sensible defaults.
#   Usage in tests: hero = make_hero(hp=10, potions=0)
#
# @pytest.fixture
# def make_hero():
#     def _make(**kwargs) -> Hero:
#         defaults = dict(name="TestHero", hero_class=HeroClass.warrior,
#                         hp=120, max_hp=120, atk=12, def_=5)
#         return Hero(**{**defaults, **kwargs})
#     return _make
