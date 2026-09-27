import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "22_filter_group_rank"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import pandas as pd
    import task

    # TODO 1: damage_per_round column
    assert "damage_per_round" in task.df.columns, (
        "Column 'damage_per_round' not found — did you add df['damage_per_round'] = ...?"
    )
    assert task.df["damage_per_round"].notna().all(), (
        "damage_per_round still contains None — replace None with the formula"
    )
    assert abs(task.df["damage_per_round"].iloc[0] - 147 / 9) < 0.01, (
        f"damage_per_round for Ada should be {147/9:.2f}, got {task.df['damage_per_round'].iloc[0]:.2f}"
    )

    # TODO 2: groupby
    assert task.avg_damage_by_class is not None, "avg_damage_by_class is still None"
    assert isinstance(task.avg_damage_by_class, pd.Series), (
        f"avg_damage_by_class should be a Series, got {type(task.avg_damage_by_class).__name__}"
    )
    assert abs(task.avg_damage_by_class["Warrior"] - 155.0) < 0.1, (
        f"Warrior avg damage should be 155.0, got {task.avg_damage_by_class['Warrior']}"
    )
    assert abs(task.avg_damage_by_class["Mage"] - 132.0) < 0.1, (
        f"Mage avg damage should be 132.0, got {task.avg_damage_by_class['Mage']}"
    )
    assert abs(task.avg_damage_by_class["Rogue"] - 139.0) < 0.1, (
        f"Rogue avg damage should be 139.0, got {task.avg_damage_by_class['Rogue']}"
    )

    # TODO 3: victory count
    assert task.victory_count is not None, "victory_count is still None"
    assert int(task.victory_count) == 6, (
        f"victory_count should be 6, got {task.victory_count}"
    )

    # TODO 4: top damage hero (catches ascending/descending mix-ups)
    assert task.top_damage_hero is not None, "top_damage_hero is still None"
    assert task.top_damage_hero == "Brom", (
        f"top_damage_hero should be 'Brom' (179 damage), got {task.top_damage_hero!r} — "
        "check the sort direction"
    )

    # TODO 5: NumPy-mask-style filter on a DataFrame
    assert isinstance(task.high_damage_heroes, pd.DataFrame), (
        f"high_damage_heroes should be a DataFrame, got {type(task.high_damage_heroes).__name__}"
    )
    assert len(task.high_damage_heroes) == 4, (
        f"high_damage_heroes should have 4 rows (damage_dealt > 150), got {len(task.high_damage_heroes)}"
    )
    assert (task.high_damage_heroes["damage_dealt"] > 150).all(), (
        "high_damage_heroes contains a row with damage_dealt <= 150 — check the threshold"
    )
    assert set(task.high_damage_heroes["hero_name"]) == {"Brom", "Dex", "Theron", "Mira"}, (
        f"high_damage_heroes should contain Brom, Dex, Theron, Mira — "
        f"got {sorted(task.high_damage_heroes['hero_name'])}"
    )

    # TODO 6: multi-column selection -> DataFrame, not Series
    assert isinstance(task.name_and_damage, pd.DataFrame), (
        f"name_and_damage should be a DataFrame (two columns selected together with [[ ]]), "
        f"got {type(task.name_and_damage).__name__}"
    )
    assert list(task.name_and_damage.columns) == ["hero_name", "damage_dealt"], (
        f"name_and_damage should have columns ['hero_name', 'damage_dealt'], "
        f"got {list(task.name_and_damage.columns)}"
    )

    _update_progress("complete")
    print("✅ Mission 22 complete: Filter, Group, Rank")
    print("   Next mission: level_1_python_basics/missions/23_plot_the_results/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
        raise SystemExit(1)
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
        raise SystemExit(1)
