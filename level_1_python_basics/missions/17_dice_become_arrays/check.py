import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "17_dice_become_arrays"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import numpy as np
    import task

    # Step 1: rolls must be a real ndarray, not a Python list
    assert isinstance(task.rolls, np.ndarray), (
        f"rolls should be a NumPy array (np.array(rolls_list)), got {type(task.rolls).__name__}"
    )
    assert list(task.rolls) == [1, 4, 6, 2], (
        f"rolls should contain [1, 4, 6, 2], got {list(task.rolls)}"
    )

    # Step 2: shape and dtype
    assert task.rolls_shape == (4,), (
        f"rolls_shape should be (4,), got {task.rolls_shape}"
    )
    assert np.issubdtype(task.rolls_dtype, np.integer), (
        f"rolls_dtype should be an integer dtype, got {task.rolls_dtype}"
    )

    # Step 3: element-wise, array -> array (catches "still a list" mistakes)
    assert isinstance(task.doubled, np.ndarray), (
        f"doubled should be a NumPy array (rolls * 2), got {type(task.doubled).__name__} — "
        "did rolls_list * 2 sneak in instead of rolls * 2?"
    )
    assert list(task.doubled) == [2, 8, 12, 4], (
        f"doubled should be [2, 8, 12, 4], got {list(task.doubled)}"
    )

    # Step 4: array + scalar
    assert isinstance(task.buffed, np.ndarray), (
        f"buffed should be a NumPy array (rolls + 1), got {type(task.buffed).__name__}"
    )
    assert list(task.buffed) == [2, 5, 7, 3], (
        f"buffed should be [2, 5, 7, 3], got {list(task.buffed)}"
    )

    # Step 5: aggregations on the small array
    assert task.total == 13, f"total should be 13, got {task.total}"
    assert abs(task.average - 3.25) < 0.001, f"average should be 3.25, got {task.average}"
    assert task.lowest == 1, f"lowest should be 1, got {task.lowest}"
    assert task.highest == 6, f"highest should be 6, got {task.highest}"

    # Step 6: the same operations, at scale
    assert isinstance(task.big_rolls, np.ndarray), (
        f"big_rolls should be a NumPy array, got {type(task.big_rolls).__name__}"
    )
    assert task.big_rolls.shape == (1000,), (
        f"big_rolls should have 1000 elements, got {task.big_rolls.shape}"
    )
    assert task.big_rolls.min() >= 1 and task.big_rolls.max() <= 6, (
        f"big_rolls should only contain values 1-6, got "
        f"min={task.big_rolls.min()} max={task.big_rolls.max()}"
    )
    assert task.big_total == int(task.big_rolls.sum()), (
        f"big_total should be {int(task.big_rolls.sum())}, got {task.big_total}"
    )
    assert abs(task.big_average - float(task.big_rolls.mean())) < 0.001, (
        f"big_average should be {task.big_rolls.mean():.4f}, got {task.big_average}"
    )
    assert task.big_lowest == int(task.big_rolls.min()), (
        f"big_lowest should be {int(task.big_rolls.min())}, got {task.big_lowest}"
    )
    assert task.big_highest == int(task.big_rolls.max()), (
        f"big_highest should be {int(task.big_rolls.max())}, got {task.big_highest}"
    )

    _update_progress("complete")
    print("✅ Mission 17 complete: Dice Become Arrays")
    print("   Next mission: level_1_python_basics/missions/18_critical_hits/README.md")


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
