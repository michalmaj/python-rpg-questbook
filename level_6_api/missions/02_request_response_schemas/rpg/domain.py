from dataclasses import dataclass
from enum import StrEnum


class HeroClass(StrEnum):
    warrior = "warrior"
    mage = "mage"
    rogue = "rogue"


@dataclass
class Hero:
    name: str
    hero_class: HeroClass
    hp: int
    max_hp: int
    atk: int
    def_: int


@dataclass
class Monster:
    name: str
    hp: int
    atk: int
    def_: int
    gold: int

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)


@dataclass
class BattleResult:
    hero_name: str
    monster_name: str
    winner: str
    rounds: int
    gold_earned: int

    def to_markdown(self) -> str:
        outcome = "Victory" if self.winner == "hero" else "Defeat"
        return (
            f"## Battle Report\n\n"
            f"**Hero:** {self.hero_name}  \n"
            f"**Monster:** {self.monster_name}  \n"
            f"**Outcome:** {outcome}  \n"
            f"**Rounds:** {self.rounds}  \n"
            f"**Gold earned:** {self.gold_earned}\n"
        )
