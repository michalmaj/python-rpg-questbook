import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "18_critical_hits"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import numpy as np
    import task

    # Part 1: critical hits (attack_rolls == 6)
    assert isinstance(task.is_critical, np.ndarray) and task.is_critical.dtype == bool, (
        f"is_critical should be a boolean array (attack_rolls == 6), "
        f"got {type(task.is_critical).__name__} with dtype "
        f"{getattr(task.is_critical, 'dtype', 'n/a')}"
    )
    assert list(task.is_critical) == [False, True, False, True, False, False, True, False], (
        f"is_critical should be [F, T, F, T, F, F, T, F] for attack_rolls == 6, "
        f"got {list(task.is_critical)}"
    )
    assert list(task.critical_rolls) == [6, 6, 6], (
        f"critical_rolls should be [6, 6, 6] (attack_rolls[is_critical]), "
        f"got {list(task.critical_rolls)}"
    )
    assert task.critical_count == 3, (
        f"critical_count should be 3, got {task.critical_count}"
    )

    # Part 2: high damage hits (damage_dealt > 20)
    assert isinstance(task.is_high_damage, np.ndarray) and task.is_high_damage.dtype == bool, (
        f"is_high_damage should be a boolean array (damage_dealt > 20), "
        f"got {type(task.is_high_damage).__name__} with dtype "
        f"{getattr(task.is_high_damage, 'dtype', 'n/a')}"
    )
    assert list(task.is_high_damage) == [False, True, False, True, False, False, True, False], (
        f"is_high_damage should be [F, T, F, T, F, F, T, F] for damage_dealt > 20, "
        f"got {list(task.is_high_damage)}"
    )
    assert list(task.high_damage_hits) == [25, 22, 28], (
        f"high_damage_hits should be [25, 22, 28], got {list(task.high_damage_hits)}"
    )
    assert task.high_damage_count == 3, (
        f"high_damage_count should be 3, got {task.high_damage_count}"
    )

    _update_progress("complete")
    print("✅ Mission 18 complete: Critical Hits")
    print("   Next mission: level_1_python_basics/missions/19_party_damage_grid/README.md")


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
