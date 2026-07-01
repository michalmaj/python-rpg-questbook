# rpg/log_repo.py
#
# Port CombatLogRepository (Protocol), CsvCombatLogRepository (from Mission 06),
# and implement SqliteCombatLogRepository.

import csv  # noqa: F401
import sqlite3  # noqa: F401
from pathlib import Path
from typing import Protocol

from rpg.schemas import CombatLogRow  # noqa: F401

FIELDNAMES = [
    "battle_id", "turn", "hero_name", "hero_class", "monster",
    "action", "damage_dealt", "damage_taken", "hero_hp", "monster_hp", "result",
]


class CombatLogRepository(Protocol):
    def append(self, row: CombatLogRow) -> None: ...
    def read_all(self) -> list[CombatLogRow]: ...


class CsvCombatLogRepository:
    """Port your Mission 06 implementation here."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, row: CombatLogRow) -> None:
        # TODO: from Mission 06
        raise NotImplementedError

    def read_all(self) -> list[CombatLogRow]:
        # TODO: from Mission 06
        raise NotImplementedError


class SqliteCombatLogRepository:
    """
    Appends and reads combat log rows from a SQLite table.

    Table schema (create in __init__ if it doesn't exist):
        combat_log (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            battle_id     INTEGER NOT NULL,
            turn          INTEGER NOT NULL,
            hero_name     TEXT NOT NULL,
            hero_class    TEXT NOT NULL,
            monster       TEXT NOT NULL,
            action        TEXT NOT NULL,
            damage_dealt  INTEGER NOT NULL,
            damage_taken  INTEGER NOT NULL,
            hero_hp       INTEGER NOT NULL,
            monster_hp    INTEGER NOT NULL,
            result        TEXT NOT NULL
        )
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        # TODO: connect and CREATE TABLE IF NOT EXISTS
        raise NotImplementedError

    def append(self, row: CombatLogRow) -> None:
        # TODO: INSERT INTO combat_log (...) VALUES (?, ?, ...)
        # Use row.model_dump() to get all field values
        raise NotImplementedError

    def read_all(self) -> list[CombatLogRow]:
        # TODO:
        # SELECT * FROM combat_log ORDER BY id
        # Convert each sqlite3.Row to CombatLogRow
        raise NotImplementedError
