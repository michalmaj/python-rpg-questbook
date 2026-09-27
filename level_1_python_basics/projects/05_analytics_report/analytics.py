"""Game Analytics Report — answer six questions about the game's data.

Each function below is one question. The check calls these functions
directly with its own data, so the exact pandas/numpy calls inside are
your choice — what matters is the return value for a given input.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]  # level_1_python_basics/, not the git repo root
M21_LOG = REPO_ROOT / "missions" / "21_from_combat_log_to_dataframe" / "sample_log.csv"
M22_LOG = REPO_ROOT / "missions" / "22_filter_group_rank" / "battles_log.csv"
PLOTS_DIR = REPO_ROOT / "plots"  # level_1_python_basics/plots/
PLOTS_DIR.mkdir(exist_ok=True)


def load_combat_log(path) -> pd.DataFrame:
    """Read a combat log CSV — columns: round, hero_hp, boss_hp."""
    return pd.read_csv(path)


def load_battles(path) -> pd.DataFrame:
    """Read a battles CSV — columns include hero_name, hero_class, damage_dealt, victory."""
    return pd.read_csv(path)


# Q1: Which class deals the highest average damage?
def avg_damage_by_class(battles_df: pd.DataFrame) -> pd.Series:
    """Mean damage_dealt per hero_class."""
    raise NotImplementedError("avg_damage_by_class")


# Q2: How many battles dealt more than `threshold` damage?
def count_above_threshold(battles_df: pd.DataFrame, threshold: int) -> int:
    """Number of rows where damage_dealt > threshold."""
    raise NotImplementedError("count_above_threshold")


# Q3: What does the damage distribution look like?
def damage_distribution(rolls) -> dict:
    """Return {"mean": ..., "std": ..., "p25": ..., "p75": ...} for an
    array-like of numbers. `rolls` may be a NumPy array or a pandas Series."""
    raise NotImplementedError("damage_distribution")


# Q4: Which class has the highest win rate?
def win_rate_by_class(battles_df: pd.DataFrame) -> pd.Series:
    """Fraction of victories (0.0-1.0) per hero_class."""
    raise NotImplementedError("win_rate_by_class")


# Bonus: who dealt the most damage of anyone?
def top_damage_hero(battles_df: pd.DataFrame) -> str:
    """hero_name of the row with the single highest damage_dealt."""
    raise NotImplementedError("top_damage_hero")


# Q5: How does HP change round to round? On which round is HP lowest?
def lowest_hp_round(combat_df: pd.DataFrame) -> int:
    """The value in the 'round' column where hero_hp is at its minimum."""
    raise NotImplementedError("lowest_hp_round")


# Q6a: Visualize HP over time.
def plot_hp_over_time(combat_df: pd.DataFrame, save_path) -> None:
    """Line chart: hero_hp and boss_hp against round. Save to save_path."""
    raise NotImplementedError("plot_hp_over_time")


# Q6b: Visualize average damage by class.
def plot_avg_damage_by_class(avg_damage: pd.Series, save_path) -> None:
    """Bar chart of avg_damage (index on the x-axis). Save to save_path."""
    raise NotImplementedError("plot_avg_damage_by_class")


if __name__ == "__main__":
    combat_df = load_combat_log(M21_LOG)
    battles_df = load_battles(M22_LOG)

    avg_damage = avg_damage_by_class(battles_df)
    win_rate = win_rate_by_class(battles_df)
    stats = damage_distribution(battles_df["damage_dealt"])

    print("=" * 50)
    print("  GAME ANALYTICS REPORT")
    print("=" * 50)

    print(f"\nAvg damage by class:\n{avg_damage.to_string()}")
    print(f"\nWin rate by class:\n{win_rate.to_string()}")
    print(f"\nDamage distribution: {stats}")
    print(f"\nBattles above 150 damage: {count_above_threshold(battles_df, 150)}")
    print(f"Top damage dealer: {top_damage_hero(battles_df)}")
    print(f"Lowest hero HP occurs on round: {lowest_hp_round(combat_df)}")

    plot_hp_over_time(combat_df, PLOTS_DIR / "report_hp.png")
    plot_avg_damage_by_class(avg_damage, PLOTS_DIR / "report_damage.png")
    print(f"\nCharts saved to: {PLOTS_DIR}")

    print("\n" + "=" * 50)
    print("  REPORT COMPLETE")
    print("=" * 50)
