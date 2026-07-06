"""Response schemas for the Monster Catalog API."""

from __future__ import annotations

from pydantic import BaseModel


class MonsterOut(BaseModel):
    name: str
    hp: int
    atk: int
    def_: int


class DifficultyOut(BaseModel):
    name: str
    difficulty: str   # "easy" | "medium" | "hard"
