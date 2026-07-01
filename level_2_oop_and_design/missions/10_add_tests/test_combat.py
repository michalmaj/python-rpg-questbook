# test_combat.py — fill in each test body.
#
# Each function tests one specific behaviour of compute_damage.
# Use assert statements. Example:
#   assert compute_damage(10, 5, 3) == 8

from combat import compute_damage  # noqa: F401


def test_normal_damage():
    # TODO: assert that compute_damage(15, 5, 4) returns 14
    pass


def test_minimum_damage_is_1():
    # TODO: assert that compute_damage with a very high defence still returns 1
    # Try: atk=1, def_=100, dice_roll=1
    pass


def test_high_roll_increases_damage():
    # TODO: assert that a dice_roll of 6 gives more damage than a roll of 1
    # Use the same atk and def_ for both calls.
    pass


def test_high_defence_reduces_damage():
    # TODO: assert that higher defence reduces damage.
    # Call compute_damage twice with the same atk and dice_roll,
    # but different def_ values. The one with higher def_ should deal less damage.
    pass


def test_damage_with_no_defence():
    # TODO: assert that compute_damage(10, 0, 5) returns 15
    pass
