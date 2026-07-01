# Mission 02: Monster Class
#
# Replace monster dictionaries with a proper Monster class.


# TODO 1: Define a Monster class.
#
# __init__ should accept: name, hp, atk, def_, gold
# Store all as instance attributes.
#
# Add these two methods:
#
#   is_alive(self) -> bool
#       Returns True if self.hp > 0.
#
#   take_damage(self, amount) -> None
#       Reduces self.hp by amount.
#       hp should never go below 0.


# TODO 2: Create these three monster objects:
#
#   goblin  — name="Goblin",  hp=30,  atk=8,  def_=2,  gold=10
#   orc     — name="Orc",     hp=55,  atk=13, def_=5,  gold=20
#   dragon  — name="Dragon",  hp=120, atk=25, def_=12, gold=60


if __name__ == "__main__":
    print(f"{goblin.name}: HP={goblin.hp}, alive={goblin.is_alive()}")  # noqa: F821

    goblin.take_damage(35)  # noqa: F821
    print(f"{goblin.name} after 35 damage: HP={goblin.hp}, alive={goblin.is_alive()}")  # noqa: F821

    print(f"{orc.name}: HP={orc.hp}")  # noqa: F821
    print(f"{dragon.name}: HP={dragon.hp}")  # noqa: F821
