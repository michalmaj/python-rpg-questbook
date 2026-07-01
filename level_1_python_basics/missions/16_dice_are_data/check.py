import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "16_dice_are_data"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import numpy as np
    import task

    assert isinstance(task.rolls, np.ndarray), (
        f"rolls should be a numpy array, got {type(task.rolls).__name__}"
    )
    assert task.rolls.shape == (1000,), (
        f"rolls should have 1000 elements, got {task.rolls.shape}"
    )
    assert task.rolls.min() >= 1 and task.rolls.max() <= 6, (
        f"rolls should only contain values 1–6, got min={task.rolls.min()} max={task.rolls.max()}"
    )

    assert task.total_damage == int(task.rolls.sum()), (
        f"total_damage should be {int(task.rolls.sum())}, got {task.total_damage}"
    )
    assert abs(task.average_roll - float(task.rolls.mean())) < 0.001, (
        f"average_roll should be {task.rolls.mean():.4f}, got {task.average_roll}"
    )
    assert task.min_roll == int(task.rolls.min()), (
        f"min_roll should be {int(task.rolls.min())}, got {task.min_roll}"
    )
    assert task.max_roll == int(task.rolls.max()), (
        f"max_roll should be {int(task.rolls.max())}, got {task.max_roll}"
    )

    _update_progress("complete")
    print("✅ Mission 16 complete: Dice Are Data")
    print("   Next mission: level_1_python_basics/missions/17_damage_distributions/README.md")


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
