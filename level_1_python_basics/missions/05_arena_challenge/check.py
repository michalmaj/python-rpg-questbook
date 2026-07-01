import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "05_arena_challenge"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    assert task.enemy_hp == 125, (
        f"enemy_hp: expected 125 after {task.rounds} rounds of 15 damage "
        f"(200 - 5×15 = 125), got {task.enemy_hp!r}"
    )
    assert task.hero_hp == 40, (
        f"hero_hp: expected 40 after {task.rounds} rounds of 12 damage "
        f"(100 - 5×12 = 40), got {task.hero_hp!r}"
    )

    _update_progress("complete")
    print("✅ Mission 05 complete: Arena Challenge")
    print("   Next mission: level_1_python_basics/missions/06_hero_inventory/README.md")


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
