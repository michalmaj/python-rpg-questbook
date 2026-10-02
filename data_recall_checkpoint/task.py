"""Data Recall Checkpoint: Combat Log Analytics.

You learned NumPy and Pandas back in Level 1. Since then the RPG gained
validation (Pydantic) and persistence (the repository pattern) in Level 3 —
including a real, validated combat log. Before moving into Level 4's
interfaces and tooling, use those data skills again on data your application
now knows how to store.

See README.md for the full brief, a short cheat-sheet, and the analytical
questions this checkpoint asks you to answer.

Check: uv run python check.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def load_combat_log(path: Path) -> pd.DataFrame:
    """Load a combat log CSV into a DataFrame.

    The CSV has one row per turn (see README for the exact column list).
    Return the full DataFrame, unfiltered — separating finished battles from
    in-progress ("ongoing") turns is the job of the functions below, not this
    one.

    TODO:
    - read the CSV at `path` with pandas
    - return the resulting DataFrame
    """
    raise NotImplementedError


def win_rate_by_class(df: pd.DataFrame) -> dict[str, float]:
    """Hero win rate per hero_class, using only finished battles.

    A battle is one `battle_id`; most battles span several turn rows, and
    only the LAST row of a battle has a terminal `result` ("win" or "loss") —
    every earlier row is "ongoing". Win rate must be computed over terminal
    rows only, grouped by `hero_class`.

    Returns a dict like {"warrior": 0.59, "mage": 0.56, "rogue": 0.78} — one
    entry per hero_class that has at least one finished battle.

    TODO:
    - keep only rows where result != "ongoing"
    - group the result by hero_class using pandas' groupby
    - for each group, compute the fraction of rows where result == "win"
    - return the per-class win rates as a plain dict
    """
    raise NotImplementedError


def damage_stats(df: pd.DataFrame) -> dict[str, float | int]:
    """NumPy statistics over attack damage.

    `action` is either "attack" or "potion". A potion turn deals no damage
    by definition (damage_dealt is 0 because the hero healed instead of
    attacking, not because the attack was weak) — including those zeros
    would understate how hard hero attacks actually hit. Only "attack" rows
    belong in this analysis.

    Using the `damage_dealt` values from attack rows as a NumPy array,
    return a dict with exactly these keys:
    - "mean": the mean damage
    - "std": the population standard deviation (i.e. plain `ndarray.std()` —
      no sample correction)
    - "p75": the 75th percentile (`np.percentile(arr, 75)`, linear
      interpolation — the default)
    - "high_damage_count": how many attack rows dealt more damage than p75

    TODO:
    - filter to action == "attack"
    - convert the damage_dealt column to a NumPy array
    - compute mean, std, and the 75th percentile with NumPy
    - build a boolean mask for damage > p75 and count it
    - return the four values in a dict
    """
    raise NotImplementedError


def rank_monsters_by_difficulty(df: pd.DataFrame) -> list[str]:
    """Rank monsters from hardest to easiest, by hero win rate.

    "Difficulty" here is only this one operational metric: the monster the
    hero beats LEAST often (lowest hero win rate, over finished battles) is
    ranked hardest. This is not a universal definition of difficulty — it
    ignores average battle length, damage exchanged, hero class matchups,
    and everything else. It is simply what this exercise asks you to
    compute.

    Return monster names ordered from hardest (lowest win rate) to easiest
    (highest win rate).

    TODO:
    - keep only finished battles
    - group by monster and compute hero win rate per monster (same idea as
      win_rate_by_class, just grouped on a different column)
    - sort the monsters by win rate, ascending
    - return the monster names as a list, in that order
    """
    raise NotImplementedError


if __name__ == "__main__":
    df = load_combat_log(DATA_DIR / "combat_log_fixture.csv")
    print(f"Loaded {len(df)} rows.")
    print("Win rate by class:", win_rate_by_class(df))
    print("Damage stats:", damage_stats(df))
    print("Monsters, hardest to easiest:", rank_monsters_by_difficulty(df))
