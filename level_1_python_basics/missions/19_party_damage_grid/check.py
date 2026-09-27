import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "19_party_damage_grid"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import numpy as np
    import task

    assert task.grid_shape == (3, 4), (
        f"grid_shape should be (3, 4), got {task.grid_shape}"
    )

    assert list(task.warrior_damage) == [12, 15, 10, 18], (
        f"warrior_damage should be [12, 15, 10, 18] (the first row), got {list(task.warrior_damage)}"
    )

    assert list(task.round_2_damage) == [15, 5, 14], (
        f"round_2_damage should be [15, 5, 14] (the second column), got {list(task.round_2_damage)}"
    )

    # Catches axis=0/axis=1 mix-ups: wrong axis gives the wrong shape or values.
    assert list(task.damage_per_hero) == [55, 66, 59], (
        f"damage_per_hero should be [55, 66, 59] (one total per hero — sum across "
        f"rounds), got {list(task.damage_per_hero)} — check which axis you summed over"
    )
    assert list(task.damage_per_round) == [46, 34, 48, 52], (
        f"damage_per_round should be [46, 34, 48, 52] (one total per round — sum "
        f"across heroes), got {list(task.damage_per_round)} — check which axis you summed over"
    )

    buffed = np.array(task.buffed_damage)
    assert buffed.shape == (3, 4), (
        f"buffed_damage should keep shape (3, 4), got {buffed.shape}"
    )
    expected_buffed = task.damage + 2
    assert (buffed == expected_buffed).all(), (
        f"buffed_damage should be the original grid with +2 on every value:\n"
        f"{expected_buffed}\ngot:\n{buffed}"
    )

    _update_progress("complete")
    print("✅ Mission 19 complete: Party Damage Grid")
    print("   Next mission: level_1_python_basics/missions/20_damage_distributions/README.md")


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
