import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "08_attack_function"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    from task import apply_damage, apply_healing

    assert apply_damage(100, 30) == 70, "apply_damage(100, 30): expected 70"
    assert apply_damage(100, 100) == 0, "apply_damage(100, 100): expected 0"
    assert apply_damage(20, 50) == 0, "apply_damage(20, 50): HP cannot go below 0"

    assert apply_healing(70, 20, 100) == 90, "apply_healing(70, 20, 100): expected 90"
    assert apply_healing(90, 20, 100) == 100, "apply_healing(90, 20, 100): expected 100 (capped at max_hp)"
    assert apply_healing(100, 20, 100) == 100, "apply_healing(100, 20, 100): already at max"

    _update_progress("complete")
    print("✅ Mission 08 complete: Attack Function")
    print("   Next mission: missions/09_dice_rolls/README.md")


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
