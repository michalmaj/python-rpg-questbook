import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "02_damage_and_healing"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    from task import apply_damage, apply_healing

    result = apply_damage(100, 30)
    assert result == 70, f"apply_damage(100, 30): expected 70, got {result}"

    result = apply_damage(100, 100)
    assert result == 0, f"apply_damage(100, 100): expected 0, got {result}"

    result = apply_damage(20, 50)
    assert result == 0, f"apply_damage(20, 50): HP cannot go below 0, got {result}"

    result = apply_healing(70, 20, 100)
    assert result == 90, f"apply_healing(70, 20, 100): expected 90, got {result}"

    result = apply_healing(90, 20, 100)
    assert result == 100, f"apply_healing(90, 20, 100): expected 100 (max_hp), got {result}"

    result = apply_healing(100, 20, 100)
    assert result == 100, f"apply_healing(100, 20, 100): already at max, got {result}"

    _update_progress("complete")
    print("✅ Mission 02 complete: Damage and Healing")
    print("   Next mission: missions/03_choose_your_hero/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
