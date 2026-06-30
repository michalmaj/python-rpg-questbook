import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "17_damage_distributions"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import numpy as np
    import task

    assert task.warrior_mean is not None, "warrior_mean is still None"
    assert task.rogue_mean is not None, "rogue_mean is still None"
    assert task.warrior_std is not None, "warrior_std is still None"
    assert task.rogue_std is not None, "rogue_std is still None"
    assert task.warrior_p25 is not None, "warrior_p25 is still None"
    assert task.warrior_p75 is not None, "warrior_p75 is still None"

    assert abs(task.warrior_mean - float(task.warrior_rolls.mean())) < 0.001, (
        f"warrior_mean should be {task.warrior_rolls.mean():.4f}, got {task.warrior_mean}"
    )
    assert abs(task.rogue_mean - float(task.rogue_rolls.mean())) < 0.001, (
        f"rogue_mean should be {task.rogue_rolls.mean():.4f}, got {task.rogue_mean}"
    )
    assert abs(task.warrior_std - float(task.warrior_rolls.std())) < 0.001, (
        f"warrior_std should be {task.warrior_rolls.std():.4f}, got {task.warrior_std}"
    )
    assert abs(task.rogue_std - float(task.rogue_rolls.std())) < 0.001, (
        f"rogue_std should be {task.rogue_rolls.std():.4f}, got {task.rogue_std}"
    )
    assert task.warrior_std > task.rogue_std, (
        "warrior_std should be greater than rogue_std — the d6 is less consistent than the d4+1"
    )

    expected_p25 = float(np.percentile(task.warrior_rolls, 25))
    expected_p75 = float(np.percentile(task.warrior_rolls, 75))
    assert abs(task.warrior_p25 - expected_p25) < 0.001, (
        f"warrior_p25 should be {expected_p25}, got {task.warrior_p25}"
    )
    assert abs(task.warrior_p75 - expected_p75) < 0.001, (
        f"warrior_p75 should be {expected_p75}, got {task.warrior_p75}"
    )

    _update_progress("complete")
    print("✅ Mission 17 complete: Damage Distributions")
    print("   Next mission: missions/18_read_combat_logs/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
