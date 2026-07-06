"""Project 01: Validated Bestiary

Load a monster catalog from a JSON file.
Validate each entry with Pydantic — a bad record must never crash the whole load.

Your task: implement the classes and functions below.
Run `uv run python check.py` from this folder to verify your work.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


# ── Domain object ─────────────────────────────────────────────────────────────

@dataclass
class MonsterDomain:
    """Plain Python object used inside the game.

    Attributes:
        name: monster display name
        hp: hit points (always positive)
        attack_type: one of "melee", "ranged", or "magic"
        gold: reward gold (zero or positive)
    """
    name: str
    hp: int
    attack_type: str
    gold: int


# ── Pydantic boundary model ───────────────────────────────────────────────────

class MonsterModel(BaseModel):
    """Validates raw JSON data before it enters the game.

    Constraints:
        name: must not be empty
        hp:   must be > 0
        gold: must be ≥ 0
        attack_type: only "melee", "ranged", or "magic" are allowed
    """
    name: str = Field(..., min_length=1)
    hp: int = Field(..., gt=0)
    attack_type: Literal["melee", "ranged", "magic"]
    gold: int = Field(..., ge=0)


# ── Converter ─────────────────────────────────────────────────────────────────

def to_domain(model: MonsterModel) -> MonsterDomain:
    """Convert a validated MonsterModel into a MonsterDomain."""
    raise NotImplementedError


# ── Loader ────────────────────────────────────────────────────────────────────

def load_bestiary(path: Path) -> tuple[list[MonsterDomain], list[str]]:
    """Load and validate a JSON monster catalog.

    Args:
        path: path to a JSON file containing a list of monster records.

    Returns:
        A 2-tuple (valid_monsters, errors) where:
        - valid_monsters: list of MonsterDomain objects that passed validation
        - errors: list of human-readable error messages for rejected records

    Rules:
        - Never raise for individual bad records — collect them in errors instead.
        - A single invalid record must not stop the rest from loading.
        - Error messages must be non-empty strings (not raw tracebacks).
    """
    raise NotImplementedError
