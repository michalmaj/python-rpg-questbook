# tests/test_combat.py
#
# Write at least 5 tests for your combat functions.
# All tests must use real assert statements (not just pass or comments).
#
# Example structure — replace the bodies with real assertions:

from rpg.combat import compute_damage  # noqa: F401


def test_normal_damage():
    # assert compute_damage(...) == ...
    pass


def test_minimum_damage_is_1():
    # assert compute_damage(very_low_atk, very_high_def, low_roll) == 1
    pass


def test_higher_roll_deals_more_damage():
    # assert compute_damage(atk, def_, high_roll) > compute_damage(atk, def_, low_roll)
    pass


def test_higher_defence_reduces_damage():
    # assert compute_damage(atk, low_def, roll) > compute_damage(atk, high_def, roll)
    pass


def test_damage_with_zero_defence():
    # assert compute_damage(10, 0, 5) == 15
    pass
