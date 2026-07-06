"""Monsters router — implement the three endpoints here.

Your task: implement list_monsters, get_monster, and get_difficulty.

Key pattern: the repository returns Monster domain objects.
The router converts them to Pydantic schemas (MonsterOut, DifficultyOut)
before returning the HTTP response.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from task.dependencies import get_monster_repo
from task.repository import Monster, MonsterRepository
from task.schemas import DifficultyOut, MonsterOut

router = APIRouter(prefix="/monsters", tags=["monsters"])


@router.get("", response_model=list[MonsterOut])
def list_monsters(repo: MonsterRepository = Depends(get_monster_repo)) -> list[MonsterOut]:
    """Return all monsters in the catalog.

    Call repo.list_all() → convert each Monster to MonsterOut.
    """
    raise NotImplementedError


@router.get("/{name}", response_model=MonsterOut)
def get_monster(name: str,
                repo: MonsterRepository = Depends(get_monster_repo)) -> MonsterOut:
    """Return one monster by name (case-insensitive).

    Call repo.get_by_name(name) → convert Monster to MonsterOut.
    Unknown name → HTTPException(status_code=404).
    """
    raise NotImplementedError


@router.get("/{name}/difficulty", response_model=DifficultyOut)
def get_difficulty(name: str,
                   repo: MonsterRepository = Depends(get_monster_repo)) -> DifficultyOut:
    """Return difficulty rating for the monster.

    Difficulty scale:
        easy   — HP ≤ 50
        medium — HP ≤ 150
        hard   — HP > 150

    Call repo.get_by_name(name) → compute difficulty from Monster.hp.
    Unknown name → HTTPException(status_code=404).
    """
    raise NotImplementedError
