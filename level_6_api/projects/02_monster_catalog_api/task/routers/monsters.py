"""Monsters router — implement the three endpoints here.

Your task: implement list_monsters, get_monster, and get_difficulty.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from task.dependencies import get_monster_repo
from task.repository import MonsterRepository
from task.schemas import DifficultyOut, MonsterOut

router = APIRouter(prefix="/monsters", tags=["monsters"])


@router.get("", response_model=list[MonsterOut])
def list_monsters(repo: MonsterRepository = Depends(get_monster_repo)) -> list[MonsterOut]:
    """Return all monsters in the catalog."""
    raise NotImplementedError


@router.get("/{name}", response_model=MonsterOut)
def get_monster(name: str,
                repo: MonsterRepository = Depends(get_monster_repo)) -> MonsterOut:
    """Return one monster by name (case-insensitive).

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

    Unknown name → HTTPException(status_code=404).
    """
    raise NotImplementedError
