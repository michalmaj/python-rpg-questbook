# rpg/domain.py — domain models (unchanged from Level 2 + missions)
# Copy Hero, HeroClass, and CombatLogRow here from your mission work.

from dataclasses import dataclass
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class HeroClass(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"


@dataclass
class Hero:
    name: str
    hero_class: HeroClass
    hp: int
    max_hp: int
    atk: int
    def_: int
    potions: int = 3
    gold: int = 0
    wins: int = 0
    losses: int = 0


class CombatLogRow(BaseModel):
    battle_id:    int = Field(ge=1)
    turn:         int = Field(ge=1)
    hero_name:    str
    hero_class:   str
    monster:      str
    action:       Literal["attack", "potion"]
    damage_dealt: int = Field(ge=0)
    damage_taken: int = Field(ge=0)
    hero_hp:      int = Field(ge=0)
    monster_hp:   int = Field(ge=0)
    result:       Literal["ongoing", "win", "loss"]
