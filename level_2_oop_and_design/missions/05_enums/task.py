# Mission 05: Enums
#
# Replace magic strings with a HeroClass enum.

from enum import Enum  # noqa: F401 — needed for your HeroClass definition below


# TODO 1: Define a HeroClass enum with three members:
#   WARRIOR = "warrior"
#   MAGE    = "mage"
#   ROGUE   = "rogue"


class Character:
    def __init__(self, name: str, hp: int, atk: int, def_: int) -> None:
        self.name  = name
        self.hp    = hp
        self.atk   = atk
        self.def_  = def_

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)


class Hero(Character):
    # TODO 2: Change the type of hero_class from str to HeroClass.
    #         Update __init__ signature and the class_bonus() method.
    def __init__(self, name: str, hp: int, atk: int, def_: int,
                 potions: int, gold: int, hero_class: str) -> None:
        super().__init__(name, hp, atk, def_)
        self.potions    = potions
        self.gold       = gold
        self.hero_class = hero_class   # TODO: change type to HeroClass

    def class_bonus(self) -> int:
        """Returns the extra attack bonus based on hero class."""
        # TODO 3: Replace string comparisons with HeroClass enum comparisons.
        if self.hero_class == "warrior":
            return 2
        elif self.hero_class == "mage":
            return 0
        elif self.hero_class == "rogue":
            return 4
        return 0


if __name__ == "__main__":
    # TODO 4: Create two heroes using HeroClass enum values (not strings).
    warrior = Hero("Ada",  hp=120, atk=15, def_=8, potions=2, gold=20,
                   hero_class="warrior")   # TODO: use HeroClass.WARRIOR
    mage    = Hero("Zara", hp=80,  atk=24, def_=3, potions=1, gold=30,
                   hero_class="mage")      # TODO: use HeroClass.MAGE

    print(f"{warrior.name} ({warrior.hero_class}): bonus = {warrior.class_bonus()}")
    print(f"{mage.name} ({mage.hero_class}): bonus = {mage.class_bonus()}")
