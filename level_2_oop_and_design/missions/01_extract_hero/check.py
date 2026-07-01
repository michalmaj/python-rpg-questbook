"""check.py — Mission 01: Extract Hero"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
PROGRESS_FILE = REPO_ROOT / "level_2_oop_and_design" / ".progress"


def update_progress(mission_id: str) -> None:
    progress = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["missions"][mission_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def main() -> None:
    try:
        from task import Hero, hero
    except ImportError as e:
        print(f"❌ Could not import from task.py: {e}")
        print("   Make sure you defined 'class Hero' and created 'hero'.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error in task.py: {e}")
        raise SystemExit(1)

    try:
        assert isinstance(hero, Hero), \
            f"'hero' should be a Hero instance, got {type(hero)}"
        assert hero.name == "Ada", \
            f"hero.name should be 'Ada', got '{hero.name}'"
        assert hero.hero_class == "warrior", \
            f"hero.hero_class should be 'warrior', got '{hero.hero_class}'"
        assert hero.hp == 120, \
            f"hero.hp should be 120, got {hero.hp}"
        assert hero.max_hp == 120, \
            f"hero.max_hp should be 120, got {hero.max_hp}"
        assert hero.atk == 15, \
            f"hero.atk should be 15, got {hero.atk}"
        assert hero.def_ == 8, \
            f"hero.def_ should be 8, got {hero.def_}"
        assert hero.potions == 2, \
            f"hero.potions should be 2, got {hero.potions}"
        assert hero.gold == 20, \
            f"hero.gold should be 20, got {hero.gold}"

        # Verify that two independent objects work
        h2 = Hero("Zara", "mage", 80, 80, 24, 3, 1, 30)
        assert h2.name == "Zara", "Two heroes should be independent objects"
        assert hero.name == "Ada", "hero.name should not change when h2 is created"

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("01_extract_hero")
    print("✅ Mission 01 complete: Hero is now a proper class!")
    print()
    print("   You replaced ten global variables with a single object.")
    print("   Next mission: level_2_oop_and_design/missions/02_monster_class/README.md")


if __name__ == "__main__":
    main()
