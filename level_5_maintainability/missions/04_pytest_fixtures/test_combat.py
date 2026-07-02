"""test_combat.py — write your tests here.

Each test function name must start with test_.
Use the fixtures defined in conftest.py as function parameters.
"""
from rpg import compute_damage, simulate_turn, Hero, HeroClass, Monster


# TODO 1: Test that compute_damage(10, 5, 3) == 8
# def test_compute_damage_normal_hit() -> None: ...


# TODO 2: Test that compute_damage(5, 10, 1) == 1  (minimum damage is always 1)
# def test_compute_damage_minimum() -> None: ...


# TODO 3: Test that Hero.take_damage reduces hp by the right amount
# Use the 'warrior' fixture from conftest.py
# def test_hero_take_damage(warrior: Hero) -> None: ...


# TODO 4: Test that Hero.use_potion heals by 30 when potions > 0
# def test_use_potion_heals(warrior: Hero) -> None: ...


# TODO 5: Test that Hero.use_potion returns False when potions == 0
# Use the make_hero factory fixture: hero = make_hero(potions=0)
# def test_use_potion_empty(make_hero) -> None: ...


# TODO 6: Test that simulate_turn kills the monster when hero deals enough damage
# Hint: use a monster with hp=1 and a hero_roll high enough to kill it in one hit
# def test_simulate_turn_hero_wins(warrior: Hero, goblin: Monster) -> None: ...
