import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "07_monster_dictionary"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    assert task.monster["name"] == "Dragon", (
        f'monster["name"]: expected "Dragon", got {task.monster["name"]!r}'
    )
    assert task.monster["damage"] == 25, (
        f'monster["damage"]: expected 25, got {task.monster["damage"]!r}'
    )
    assert task.monster["reward"] == 100, (
        f'monster["reward"]: expected 100, got {task.monster["reward"]!r}'
    )
    assert task.monster["hp"] == 120, (
        f'monster["hp"]: expected 120 after 30 damage (150 - 30 = 120), '
        f'got {task.monster["hp"]!r}'
    )

    _update_progress("complete")
    print("✅ Mission 07 complete: Monster Dictionary")
    print("   Next mission: missions/08_attack_function/README.md")


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
