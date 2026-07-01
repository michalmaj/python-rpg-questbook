# combat.py — provided and complete. Do not modify.

import random


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    """Return damage: atk + dice_roll - def_, minimum 1."""
    return max(1, atk + dice_roll - def_)


def resolve_hit(atk: int, def_: int) -> int:
    """Roll a d6 then compute damage."""
    return compute_damage(atk, def_, random.randint(1, 6))
