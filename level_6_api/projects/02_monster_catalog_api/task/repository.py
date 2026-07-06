"""Monster repository — domain object + Protocol + in-memory implementation.

Your task: implement InMemoryMonsterRepository.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


# ── Domain model (not Pydantic — no HTTP coupling) ───────────────────────────

@dataclass
class Monster:
    """Pure domain object. The router converts this to MonsterOut for HTTP responses."""
    name: str
    hp: int
    atk: int
    def_: int


# ── Hardcoded catalog ─────────────────────────────────────────────────────────

_CATALOG: list[dict] = [
    {"name": "Goblin", "hp": 30,  "atk": 8,  "def_": 2},
    {"name": "Orc",    "hp": 60,  "atk": 12, "def_": 4},
    {"name": "Troll",  "hp": 100, "atk": 18, "def_": 6},
    {"name": "Dragon", "hp": 200, "atk": 30, "def_": 10},
]


# ── Protocol ──────────────────────────────────────────────────────────────────

class MonsterRepository(Protocol):
    def list_all(self) -> list[Monster]: ...
    def get_by_name(self, name: str) -> Monster | None: ...


# ── In-memory implementation ──────────────────────────────────────────────────

class InMemoryMonsterRepository:
    """Loads from the hardcoded catalog above.

    Implement list_all() and get_by_name().
    Both return Monster domain objects — the router converts them to MonsterOut.
    get_by_name() should be case-insensitive.
    """

    def list_all(self) -> list[Monster]:
        raise NotImplementedError

    def get_by_name(self, name: str) -> Monster | None:
        raise NotImplementedError
