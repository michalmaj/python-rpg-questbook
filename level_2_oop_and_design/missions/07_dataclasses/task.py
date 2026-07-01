# Mission 07: Dataclasses
#
# Replace the hand-written MonsterTemplate class with a @dataclass.

from dataclasses import dataclass  # noqa: F401


# TODO 1: Add @dataclass to MonsterTemplate.
#         Replace the __init__ method with type-annotated class-level fields:
#           name:  str
#           hp:    int
#           atk:   int
#           def_:  int
#           gold:  int
#
#         Delete the existing __init__ — the decorator will generate one.

class MonsterTemplate:
    def __init__(self, name: str, hp: int, atk: int, def_: int, gold: int) -> None:
        self.name  = name
        self.hp    = hp
        self.atk   = atk
        self.def_  = def_
        self.gold  = gold


# TODO 2: Create four MonsterTemplate instances using the data from the legacy MONSTERS table:
#   goblin_template  — name="Goblin",  hp=30,  atk=8,  def_=2,  gold=10
#   orc_template     — name="Orc",     hp=55,  atk=13, def_=5,  gold=20
#   troll_template   — name="Troll",   hp=80,  atk=18, def_=8,  gold=35
#   dragon_template  — name="Dragon",  hp=120, atk=25, def_=12, gold=60


if __name__ == "__main__":
    # @dataclass generates __repr__ automatically — no need to write it
    print(goblin_template)  # noqa: F821
    print(orc_template)  # noqa: F821
    print(troll_template)  # noqa: F821
    print(dragon_template)  # noqa: F821

    # @dataclass generates __eq__ — compare two equal templates
    goblin2 = MonsterTemplate(name="Goblin", hp=30, atk=8, def_=2, gold=10)
    print(f"\ngoblin_template == goblin2: {goblin_template == goblin2}")  # noqa: F821
