import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "09_shared_inventory"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    assert task.fixed_recruit_kit is not task.fixed_starter_kit, (
        "fixed_recruit_kit and fixed_starter_kit are still the same list object — "
        "use .copy(), list(...), or [:] to make an independent copy."
    )
    assert task.fixed_starter_kit == ["dagger", "torch", "rations"], (
        f"fixed_starter_kit should be unchanged after the recruit's kit was modified, "
        f"got {task.fixed_starter_kit!r} — did you accidentally still alias it?"
    )
    assert task.fixed_recruit_kit == ["dagger", "torch", "rations", "shield"], (
        f"fixed_recruit_kit should be the starter kit plus 'shield', "
        f"got {task.fixed_recruit_kit!r}"
    )

    _update_progress("complete")
    print("✅ Mission 09 complete: Shared Inventory")
    print("   Next mission: level_1_python_basics/missions/10_dice_rolls/README.md")


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
