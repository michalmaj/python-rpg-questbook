import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "18_read_combat_logs"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import pandas as pd
    import task

    assert isinstance(task.df, pd.DataFrame), (
        f"df should be a DataFrame, got {type(task.df).__name__} — did you call pd.read_csv()?"
    )
    assert task.df.shape == (9, 3), (
        f"df should have 9 rows and 3 columns, got {task.df.shape}"
    )
    assert list(task.df.columns) == ["round", "hero_hp", "boss_hp"], (
        f"Columns should be ['round', 'hero_hp', 'boss_hp'], got {list(task.df.columns)}"
    )

    expected_avg = float(task.df["hero_hp"].mean())
    assert task.avg_hero_hp is not None, "avg_hero_hp is still None"
    assert abs(task.avg_hero_hp - expected_avg) < 0.01, (
        f"avg_hero_hp should be {expected_avg:.2f}, got {task.avg_hero_hp}"
    )

    expected_min = int(task.df["hero_hp"].min())
    assert task.min_hero_hp is not None, "min_hero_hp is still None"
    assert int(task.min_hero_hp) == expected_min, (
        f"min_hero_hp should be {expected_min}, got {task.min_hero_hp}"
    )

    assert task.final_round is not None, "final_round is still None"
    assert int(task.final_round) == 9, (
        f"final_round should be 9, got {task.final_round}"
    )

    _update_progress("complete")
    print("✅ Mission 18 complete: Read Combat Logs")
    print("   Next mission: missions/19_filter_and_group/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
