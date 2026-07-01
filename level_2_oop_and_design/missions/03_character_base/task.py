# Mission 03: Character Base
#
# Hero and Monster share duplicated logic. Extract it into a base class.


# TODO 1: Define a Character base class with:
#   __init__(self, name, hp, atk, def_) — store all as attributes
#   is_alive(self) -> bool              — returns True if hp > 0
#   take_damage(self, amount) -> None   — reduces hp, never below 0


# TODO 2: Define Hero(Character) with:
#   __init__(self, name, hp, atk, def_, potions, gold)
#   Call super().__init__(name, hp, atk, def_)
#   Store potions and gold as hero-specific attributes.


# TODO 3: Define Monster(Character) with:
#   __init__(self, name, hp, atk, def_, gold)
#   Call super().__init__(name, hp, atk, def_)
#   Store gold as a monster-specific attribute.


if __name__ == "__main__":
    hero    = Hero("Ada", hp=120, atk=15, def_=8, potions=2, gold=20)  # noqa: F821
    goblin  = Monster("Goblin", hp=30, atk=8, def_=2, gold=10)  # noqa: F821

    print(f"Hero:    {hero.name}, HP={hero.hp}, alive={hero.is_alive()}")
    print(f"Monster: {goblin.name}, HP={goblin.hp}, alive={goblin.is_alive()}")

    goblin.take_damage(25)
    print(f"After 25 damage: Goblin HP={goblin.hp}, alive={goblin.is_alive()}")

    goblin.take_damage(100)
    print(f"After 100 more damage: Goblin HP={goblin.hp} (should be 0)")
