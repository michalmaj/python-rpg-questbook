# rpg/monster.py — Monster class and templates (already complete, provided for you)

from dataclasses import dataclass


@dataclass
class MonsterTemplate:
    name: str
    hp:   int
    atk:  int
    def_: int
    gold: int


class Monster:
    def __init__(self, template: MonsterTemplate) -> None:
        self.name: str = template.name
        self.hp:   int = template.hp
        self.atk:  int = template.atk
        self.def_: int = template.def_
        self.gold: int = template.gold

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def __repr__(self) -> str:
        return f"Monster(name={self.name!r}, hp={self.hp})"


MONSTER_TEMPLATES: list[MonsterTemplate] = [
    MonsterTemplate("Goblin", hp=30,  atk=8,  def_=2,  gold=10),
    MonsterTemplate("Orc",    hp=55,  atk=13, def_=5,  gold=20),
    MonsterTemplate("Troll",  hp=80,  atk=18, def_=8,  gold=35),
    MonsterTemplate("Dragon", hp=120, atk=25, def_=12, gold=60),
]
