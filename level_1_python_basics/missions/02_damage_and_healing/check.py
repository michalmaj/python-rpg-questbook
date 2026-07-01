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
    import task

    assert task.hp_after_attack == 70, (
        f"hp_after_attack: expected 70 (100 - 30), got {task.hp_after_attack!r}"
    )
    assert task.hp_after_healing == 90, (
        f"hp_after_healing: expected 90 (70 + 20), got {task.hp_after_healing!r}"
    )
    assert task.hp_after_big_hit == 0, (
        f"hp_after_big_hit: expected 0 (cannot go below 0), got {task.hp_after_big_hit!r}"
    )

    _update_progress("complete")
    print("✅ Mission 02 complete: Damage and Healing")
    print("   Next mission: missions/03_choose_your_hero/README.md")


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
