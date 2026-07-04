"""Mission 01: Blocking vs Background Work.

Goal:  See why long-running work blocks the application.
       Instrument simulate_tournament() to measure how long it takes.
Check: uv run python check.py
"""
import time
from pathlib import Path

from rpg.repositories import MonsterRepository
from rpg.services import SimulationService

_DATA = Path(__file__).parent / "data"
_svc = SimulationService(MonsterRepository(_DATA / "monsters.json"))


def time_tournament(n: int) -> dict:
    """TODO: run _svc.simulate_tournament(n), measure wall-clock time,
    return dict with keys: battles (int), time_seconds (float), battles_per_second (float).
    """
    raise NotImplementedError
