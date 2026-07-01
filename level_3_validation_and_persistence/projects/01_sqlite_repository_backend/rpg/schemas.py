# rpg/schemas.py — Pydantic boundary models
#
# These live at the boundary between external data and the domain.
# They validate data coming in (JSON, CSV, SQLite rows) and serialise
# data going out. The domain (rpg/domain.py) never imports from here.

from typing import Literal

from pydantic import BaseModel, Field

CURRENT_SCHEMA_VERSION = 1


class SaveGameModel(BaseModel):
    """Validated representation of save_game.json / saves table row."""

    schema_version: int = Field(default=CURRENT_SCHEMA_VERSION, ge=1)
    name:       str
    hero_class: str
    hp:         int = Field(ge=0)
    max_hp:     int = Field(gt=0)
    atk:        int = Field(ge=1)
    def_:       int = Field(ge=0)
    potions:    int = Field(ge=0)
    gold:       int = Field(ge=0)
    wins:       int = Field(ge=0)
    losses:     int = Field(ge=0)


class CombatLogRow(BaseModel):
    """Validated representation of one combat turn (CSV row / DB row)."""

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
