import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "09_dice_rolls"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    assert task.hero_roll is not None, (
        "hero_roll is None — did you call random.randint(1, 6)?"
    )
    assert 1 <= task.hero_roll <= 6, (
        f"hero_roll: expected a value from 1 to 6, got {task.hero_roll!r} — "
        "use random.randint(1, 6)"
    )
    assert task.hero_damage == task.hero_roll * 3, (
        f"hero_damage: expected {task.hero_roll * 3} (hero_roll × 3), "
        f"got {task.hero_damage!r}"
    )

    assert task.monster_roll is not None, (
        "monster_roll is None — did you call random.randint(1, 4)?"
    )
    assert 1 <= task.monster_roll <= 4, (
        f"monster_roll: expected a value from 1 to 4, got {task.monster_roll!r} — "
        "use random.randint(1, 4)"
    )
    assert task.monster_damage == task.monster_roll * 2, (
        f"monster_damage: expected {task.monster_roll * 2} (monster_roll × 2), "
        f"got {task.monster_damage!r}"
    )

    _update_progress("complete")
    print("✅ Mission 09 complete: Dice Rolls")
    print("   Next mission: missions/10_safe_input/README.md")


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
