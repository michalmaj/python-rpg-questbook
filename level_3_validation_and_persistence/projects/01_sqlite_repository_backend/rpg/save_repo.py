# rpg/save_repo.py
#
# Port SaveRepository (Protocol), JsonSaveRepository (from Mission 05),
# and implement SqliteSaveRepository.
#
# SaveGameModel is provided below — same as Mission 04.

import json  # noqa: F401
import sqlite3  # noqa: F401
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, Field

from rpg.domain import Hero, HeroClass  # noqa: F401

CURRENT_SCHEMA_VERSION = 1


class SaveGameModel(BaseModel):
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

    def to_hero(self) -> Hero:
        return Hero(
            name=self.name,
            hero_class=HeroClass(self.hero_class),
            hp=self.hp,
            max_hp=self.max_hp,
            atk=self.atk,
            def_=self.def_,
            potions=self.potions,
            gold=self.gold,
            wins=self.wins,
            losses=self.losses,
        )

    @classmethod
    def from_hero(cls, hero: Hero) -> "SaveGameModel":
        return cls(
            name=hero.name,
            hero_class=hero.hero_class.value,
            hp=hero.hp,
            max_hp=hero.max_hp,
            atk=hero.atk,
            def_=hero.def_,
            potions=hero.potions,
            gold=hero.gold,
            wins=hero.wins,
            losses=hero.losses,
        )


class SaveRepository(Protocol):
    def save(self, hero: Hero) -> None: ...
    def load(self) -> Hero | None: ...


class JsonSaveRepository:
    """Port your Mission 05 implementation here."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, hero: Hero) -> None:
        # TODO: from Mission 05
        raise NotImplementedError

    def load(self) -> Hero | None:
        # TODO: from Mission 05
        raise NotImplementedError


class SqliteSaveRepository:
    """
    Saves and loads a Hero as a single row in a SQLite database.

    Table schema (create in __init__ if it doesn't exist):
        saves (
            id         INTEGER PRIMARY KEY,   -- always 1
            schema_ver INTEGER NOT NULL,
            hero_json  TEXT NOT NULL           -- SaveGameModel.model_dump_json()
        )
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        # TODO: connect and CREATE TABLE IF NOT EXISTS
        raise NotImplementedError

    def save(self, hero: Hero) -> None:
        # TODO:
        # 1. model = SaveGameModel.from_hero(hero)
        # 2. INSERT OR REPLACE INTO saves VALUES (1, schema_version, model.model_dump_json())
        raise NotImplementedError

    def load(self) -> Hero | None:
        # TODO:
        # 1. SELECT schema_ver, hero_json FROM saves WHERE id = 1
        # 2. If no row → return None
        # 3. If schema_ver != CURRENT_SCHEMA_VERSION → raise ValueError
        # 4. return SaveGameModel.model_validate_json(hero_json).to_hero()
        raise NotImplementedError
