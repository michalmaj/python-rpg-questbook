"""Project 01: Async Quest Aggregator

Fetch quests from three sources concurrently using asyncio.
A source that times out or errors must not block the others.

Your task: implement aggregate_all_quests().
Run `uv run python check.py` to verify your work.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field


# ── Domain ────────────────────────────────────────────────────────────────────

@dataclass
class Quest:
    title: str
    source: str       # "guild" | "village" | "royal"
    reward_gold: int


@dataclass
class AggregateResult:
    quests: list[Quest]
    failed_sources: list[str]   # sources that timed out or errored
    elapsed: float              # wall-clock seconds (time.monotonic)


# ── Pre-implemented sources (do not modify) ───────────────────────────────────

async def fetch_guild_quests() -> list[Quest]:
    await asyncio.sleep(0.1)
    return [
        Quest("Slay the Goblin", "guild", 50),
        Quest("Guard the Merchant", "guild", 80),
    ]


async def fetch_village_quests() -> list[Quest]:
    await asyncio.sleep(0.05)
    return [
        Quest("Retrieve the Lost Cow", "village", 20),
    ]


async def fetch_royal_quests() -> list[Quest]:
    await asyncio.sleep(0.2)
    return [
        Quest("Escort the Ambassador", "royal", 300),
        Quest("Investigate the Catacombs", "royal", 250),
    ]


# ── Your implementation ───────────────────────────────────────────────────────

SOURCES: dict[str, object] = {
    "guild":   fetch_guild_quests,
    "village": fetch_village_quests,
    "royal":   fetch_royal_quests,
}


async def aggregate_all_quests(timeout: float) -> AggregateResult:
    """Fetch quests from all three sources concurrently.

    Args:
        timeout: per-source timeout in seconds.
                 Sources that exceed this limit go into failed_sources.

    Returns:
        AggregateResult with all successfully fetched quests merged,
        failed source names, and total elapsed time.

    Requirements:
        - Use asyncio.gather(..., return_exceptions=True)
        - Wrap each source with asyncio.wait_for(..., timeout=timeout)
        - A TimeoutError or other exception → source name goes to failed_sources
        - Successful sources → their quests merged into the quests list
        - No sequential awaits — all three fetches must run concurrently
    """
    raise NotImplementedError
