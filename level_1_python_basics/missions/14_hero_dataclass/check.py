import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "14_hero_dataclass"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    hero = task.hero

    assert hero.name == "Ada", f"hero.name: expected 'Ada', got {hero.name!r}"
    assert hero.hero_class == "Warrior", f"hero.hero_class: expected 'Warrior', got {hero.hero_class!r}"
    assert hero.hp == 70, f"hero.hp: expected 70 (100 - 30), got {hero.hp}"
    assert hero.max_hp == 100, f"hero.max_hp: expected 100, got {hero.max_hp}"
    assert hero.level == 1, f"hero.level: expected 1, got {hero.level}"
    assert hero.gold == 75, f"hero.gold: expected 75 (50 + 25), got {hero.gold}"

    _update_progress("complete")
    print("✅ Mission 14 complete: Hero Dataclass")
    print("   Next mission: level_1_python_basics/missions/15_test_the_damage/README.md")


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
