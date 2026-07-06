"""Project 02: Save Slot Manager

A repository-backed save system with three slots.
Implement the Pydantic model, the Protocol, and two concrete repositories.

Your task: implement everything below.
Run `uv run python check.py` from this folder to verify your work.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from pydantic import BaseModel, Field


# ── Pydantic boundary model ───────────────────────────────────────────────────

class SaveGameModel(BaseModel):
    """A validated save-game snapshot.

    Attributes:
        schema_version: bumped when the format changes (start at 1)
        slot:           save slot number (1, 2, or 3)
        hero_name:      name of the saved hero
        hero_hp:        current hit points
        level:          hero level
        gold:           gold carried
    """
    schema_version: int = 1
    slot: int = Field(..., ge=1, le=3)
    hero_name: str
    hero_hp: int
    level: int
    gold: int


# ── Repository Protocol ───────────────────────────────────────────────────────

@runtime_checkable
class SaveRepository(Protocol):
    """Interface every save backend must satisfy."""

    def save(self, model: SaveGameModel) -> None:
        """Persist the save game for the given slot."""
        ...

    def load(self, slot: int) -> SaveGameModel | None:
        """Return the save game for slot, or None if the slot is empty."""
        ...

    def list_slots(self) -> list[int]:
        """Return a sorted list of occupied slot numbers."""
        ...

    def delete(self, slot: int) -> None:
        """Remove the save game for slot. No-op if the slot is already empty."""
        ...


# ── JSON backend ──────────────────────────────────────────────────────────────

class JsonSaveRepository:
    """Stores each slot as a separate JSON file named slot_{n}.json.

    Args:
        directory: folder where slot files are written.
    """

    def __init__(self, directory: Path) -> None:
        raise NotImplementedError

    def save(self, model: SaveGameModel) -> None:
        raise NotImplementedError

    def load(self, slot: int) -> SaveGameModel | None:
        raise NotImplementedError

    def list_slots(self) -> list[int]:
        raise NotImplementedError

    def delete(self, slot: int) -> None:
        raise NotImplementedError


# ── In-memory backend (for tests) ────────────────────────────────────────────

class InMemorySaveRepository:
    """Dict-backed repository — no disk I/O.

    Useful in tests and for unit-level verification of game logic.
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def save(self, model: SaveGameModel) -> None:
        raise NotImplementedError

    def load(self, slot: int) -> SaveGameModel | None:
        raise NotImplementedError

    def list_slots(self) -> list[int]:
        raise NotImplementedError

    def delete(self, slot: int) -> None:
        raise NotImplementedError
