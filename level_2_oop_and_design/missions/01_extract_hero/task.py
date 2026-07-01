# Mission 01: Extract Hero
#
# The legacy RPG uses ten global variables for the hero.
# Your job: collect them into a Hero class.


# TODO 1: Define a Hero class.
#
# It should have an __init__ that accepts:
#   name, hero_class, hp, max_hp, atk, def_, potions, gold
#
# Store each argument as an instance attribute.
# Use the same names as the parameters (self.name = name, etc.)
#
# Note: 'def' is a Python keyword, so the parameter is named 'def_'
#       but the attribute should be stored as self.def_ as well.


# TODO 2: Create a warrior hero object named 'hero':
#   name="Ada", hero_class="warrior", hp=120, max_hp=120,
#   atk=15, def_=8, potions=2, gold=20


if __name__ == "__main__":
    print(f"Name:    {hero.name}")  # noqa: F821
    print(f"Class:   {hero.hero_class}")  # noqa: F821
    print(f"HP:      {hero.hp}/{hero.max_hp}")  # noqa: F821
    print(f"ATK:     {hero.atk}  DEF: {hero.def_}")  # noqa: F821
    print(f"Potions: {hero.potions}  Gold: {hero.gold}")  # noqa: F821
