import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "01_hero_stats"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    assert task.hero_name == "Ada", f'hero_name: expected "Ada", got {task.hero_name!r}'
    assert task.hero_hp == 100, f"hero_hp: expected 100, got {task.hero_hp!r}"
    assert task.hero_damage == 15, f"hero_damage: expected 15, got {task.hero_damage!r}"
    assert task.hero_gold == 50, f"hero_gold: expected 50, got {task.hero_gold!r}"

    _update_progress("complete")
    print("✅ Mission 01 complete: Hero Stats")
    print("   Next mission: level_1_python_basics/missions/02_damage_and_healing/README.md")


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
