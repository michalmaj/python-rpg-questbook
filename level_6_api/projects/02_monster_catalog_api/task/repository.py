"""Monster repository — Protocol + in-memory implementation.

Your task: implement InMemoryMonsterRepository.
"""

from __future__ import annotations

from typing import Protocol

from task.schemas import MonsterOut

# ── Hardcoded catalog ─────────────────────────────────────────────────────────

_CATALOG: list[dict] = [
    {"name": "Goblin", "hp": 30,  "atk": 8,  "def_": 2},
    {"name": "Orc",    "hp": 60,  "atk": 12, "def_": 4},
    {"name": "Troll",  "hp": 100, "atk": 18, "def_": 6},
    {"name": "Dragon", "hp": 200, "atk": 30, "def_": 10},
]


# ── Protocol ──────────────────────────────────────────────────────────────────

class MonsterRepository(Protocol):
    def list_all(self) -> list[MonsterOut]: ...
    def get_by_name(self, name: str) -> MonsterOut | None: ...


# ── In-memory implementation ──────────────────────────────────────────────────

class InMemoryMonsterRepository:
    """Loads from the hardcoded catalog above.

    Implement list_all() and get_by_name().
    get_by_name() should be case-insensitive.
    """

    def list_all(self) -> list[MonsterOut]:
        raise NotImplementedError

    def get_by_name(self, name: str) -> MonsterOut | None:
        raise NotImplementedError
