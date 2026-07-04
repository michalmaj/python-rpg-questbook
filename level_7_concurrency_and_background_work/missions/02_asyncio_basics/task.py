"""Mission 02: asyncio Basics.

Goal:  Learn async/await, asyncio.gather, and asyncio.wait_for.
       These are the building blocks for non-blocking I/O in Python.
Check: uv run python check.py
"""
import asyncio


async def fetch_monster_data(name: str) -> dict:
    """TODO: simulate a slow database/API call using asyncio.sleep(0.05).
    Return {"name": name, "fetched": True}.
    """
    raise NotImplementedError


async def fetch_all_monsters(names: list[str]) -> list[dict]:
    """TODO: use asyncio.gather to fetch all monsters CONCURRENTLY.
    Each fetch_monster_data() call is a fake I/O operation.
    Concurrent fetches should finish in ~0.05s, not n*0.05s.
    """
    raise NotImplementedError


async def fetch_with_timeout(name: str, timeout: float) -> dict | None:
    """TODO: use asyncio.wait_for to fetch a monster with a timeout.
    Return the result if it completes in time, or None on timeout.
    """
    raise NotImplementedError
