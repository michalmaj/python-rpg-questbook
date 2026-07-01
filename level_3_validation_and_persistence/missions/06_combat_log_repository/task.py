"""
Mission 06: Combat Log Repository

The starter RPG logs combat rows directly inside run_combat():

    with open(LOG_PATH, "a") as f:
        writer.writerow([battle_id, turn, ...])

This couples the combat loop to the CSV format and the file path.
If you want to:
  - Write tests that check what was logged without reading a file
  - Change the format to JSON Lines or a database
  - Log to two places at once

...you must dig into run_combat() and change it.

The fix: a CombatLogRepository that run_combat() calls.
Game code appends rows; it doesn't know the format or destination.

Your task: define CombatLogRow, CombatLogRepository (Protocol),
and implement CsvCombatLogRepository.
"""

import csv  # noqa: F401
from pathlib import Path
from typing import Literal, Protocol

from pydantic import BaseModel, Field

LOG_DIR = Path(__file__).parent / "logs"


# ----- Pydantic log row model -------------------------------------------------


class CombatLogRow(BaseModel):
    """One turn in a battle, validated on the way in."""

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


# ----- Protocol ---------------------------------------------------------------


class CombatLogRepository(Protocol):
    def append(self, row: CombatLogRow) -> None:
        """Add one turn to the log."""
        ...

    def read_all(self) -> list[CombatLogRow]:
        """Return all logged turns."""
        ...


# ----- CSV implementation -----------------------------------------------------

FIELDNAMES = [
    "battle_id", "turn", "hero_name", "hero_class", "monster",
    "action", "damage_dealt", "damage_taken", "hero_hp", "monster_hp", "result",
]


class CsvCombatLogRepository:
    """Appends combat rows to a CSV file; reads them back as validated models."""

    def __init__(self, path: Path = LOG_DIR / "combat_log.csv") -> None:
        self.path = path

    def append(self, row: CombatLogRow) -> None:
        # TODO:
        # 1. Create parent directories if needed
        # 2. Determine whether to write a header (only if file does not exist yet)
        # 3. Open the file in append mode ("a", newline="")
        # 4. Write the header row if needed
        # 5. Write the data row using row.model_dump()
        #    Hint: csv.DictWriter(f, fieldnames=FIELDNAMES)
        raise NotImplementedError

    def read_all(self) -> list[CombatLogRow]:
        # TODO:
        # 1. Return [] if self.path does not exist
        # 2. Open the file and use csv.DictReader to read rows
        # 3. For each dict row, convert int/str fields to correct types
        #    Hint: the CSV stores everything as strings —
        #          use CombatLogRow.model_validate(row_dict) to parse+validate
        # 4. Return the list of CombatLogRow objects
        raise NotImplementedError


# ----- in-memory implementation (for tests) -----------------------------------


class InMemoryCombatLogRepository:
    """
    Stores combat rows in a list — no files.
    Use this in tests so you can check what was logged without touching disk.
    """

    def __init__(self) -> None:
        self._rows: list[CombatLogRow] = []

    def append(self, row: CombatLogRow) -> None:
        # TODO: add row to self._rows
        raise NotImplementedError

    def read_all(self) -> list[CombatLogRow]:
        # TODO: return a copy of self._rows
        raise NotImplementedError


# ----- runner -----------------------------------------------------------------


def main() -> None:
    log_path = LOG_DIR / "combat_log.csv"
    repo = CsvCombatLogRepository(log_path)

    # Simulate two combat turns
    row1 = CombatLogRow(
        battle_id=1, turn=1,
        hero_name="Ada", hero_class="warrior", monster="Goblin",
        action="attack", damage_dealt=12, damage_taken=4,
        hero_hp=96, monster_hp=18, result="ongoing",
    )
    row2 = CombatLogRow(
        battle_id=1, turn=2,
        hero_name="Ada", hero_class="warrior", monster="Goblin",
        action="attack", damage_dealt=18, damage_taken=0,
        hero_hp=96, monster_hp=0, result="win",
    )

    repo.append(row1)
    repo.append(row2)

    rows = repo.read_all()
    print(f"Logged {len(rows)} turns:")
    for r in rows:
        print(f"  Turn {r.turn}: {r.action}, dealt={r.damage_dealt}, result={r.result}")


if __name__ == "__main__":
    main()
