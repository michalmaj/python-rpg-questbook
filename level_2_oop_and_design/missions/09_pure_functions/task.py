# Mission 09: Pure Functions
#
# Extract the damage calculation from the impure hero_attacks() into
# pure functions that are easy to test.

import random


# TODO 1: Define compute_damage(atk: int, def_: int, dice_roll: int) -> int
#
#   Formula: atk + dice_roll - def_
#   Return at least 1 (damage can never be 0 or negative).
#   This function must NOT call random.randint — the caller provides the roll.
#   This function must NOT print anything.


# TODO 2: Define resolve_hit(atk: int, def_: int) -> int
#
#   Roll a d6 (random.randint(1, 6)), then call compute_damage with the result.
#   Return the damage.
#   This function may call random, but must NOT print anything.


# ── Do not modify the function below — it is the impure original ──────────────

hero_name = "Ada"
hero_atk  = 15

def hero_attacks_legacy(monster: dict) -> None:
    """Original impure function from the legacy RPG. Left here for comparison."""
    dmg = hero_atk + random.randint(1, 6) - monster["def"]
    if dmg < 1:
        dmg = 1
    print(f"  {hero_name} attacks for {dmg} damage.")
    monster["hp"] -= dmg


if __name__ == "__main__":
    # Test compute_damage with known inputs — no randomness  # noqa: F821
    dmg = compute_damage(atk=15, def_=5, dice_roll=4)  # noqa: F821
    print(f"compute_damage(15, 5, 4) = {dmg}  (expected 14)")  # noqa: F821

    dmg_floored = compute_damage(atk=5, def_=20, dice_roll=1)  # noqa: F821
    print(f"compute_damage(5, 20, 1) = {dmg_floored}  (expected 1 — minimum)")  # noqa: F821

    # resolve_hit uses real randomness  # noqa: F821
    for _ in range(3):
        dmg = resolve_hit(atk=15, def_=5)  # noqa: F821
        print(f"resolve_hit(15, 5) = {dmg}")  # noqa: F821
