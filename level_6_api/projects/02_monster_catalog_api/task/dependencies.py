"""Dependency factories — injected via Depends()."""

from __future__ import annotations

from task.repository import InMemoryMonsterRepository, MonsterRepository


def get_monster_repo() -> MonsterRepository:
    """Return the default monster repository.

    Used as: repo: MonsterRepository = Depends(get_monster_repo)
    """
    return InMemoryMonsterRepository()
