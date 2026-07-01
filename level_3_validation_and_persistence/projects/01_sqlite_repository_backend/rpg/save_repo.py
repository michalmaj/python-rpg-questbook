# rpg/save_repo.py
#
# Port SaveRepository (Protocol), JsonSaveRepository (from Mission 05),
# and implement SqliteSaveRepository.
#
# SaveGameModel lives in rpg/schemas.py (boundary models).
# This module adds to_hero() / from_hero() as module-level helpers
# so save_repo.py stays decoupled from Pydantic details.

import json  # noqa: F401
import sqlite3  # noqa: F401
from pathlib import Path
from typing import Protocol

from rpg.domain import Hero, HeroClass
from rpg.schemas import CURRENT_SCHEMA_VERSION, SaveGameModel  # noqa: F401


def _model_to_hero(model: SaveGameModel) -> Hero:
    return Hero(
        name=model.name,
        hero_class=HeroClass(model.hero_class),
        hp=model.hp,
        max_hp=model.max_hp,
        atk=model.atk,
        def_=model.def_,
        potions=model.potions,
        gold=model.gold,
        wins=model.wins,
        losses=model.losses,
    )


def _hero_to_model(hero: Hero) -> SaveGameModel:
    return SaveGameModel(
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
