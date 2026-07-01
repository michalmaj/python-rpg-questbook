"""check.py — Mission 05: Enums"""

import json
from enum import Enum
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
PROGRESS_FILE = REPO_ROOT / "level_2_oop_and_design" / ".progress"


def update_progress(mission_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
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
        from task import HeroClass, Hero
    except ImportError as e:
        print(f"❌ Could not import from task.py: {e}")
        print("   Make sure you defined 'class HeroClass(Enum)' and updated 'Hero'.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error in task.py: {e}")
        raise SystemExit(1)

    try:
        # HeroClass is a proper Enum
        assert issubclass(HeroClass, Enum), "HeroClass should inherit from Enum"
        assert hasattr(HeroClass, "WARRIOR"), "HeroClass should have WARRIOR"
        assert hasattr(HeroClass, "MAGE"),    "HeroClass should have MAGE"
        assert hasattr(HeroClass, "ROGUE"),   "HeroClass should have ROGUE"

        # Values
        assert HeroClass.WARRIOR.value == "warrior", \
            f"HeroClass.WARRIOR.value should be 'warrior', got '{HeroClass.WARRIOR.value}'"
        assert HeroClass.MAGE.value == "mage"
        assert HeroClass.ROGUE.value == "rogue"

        # Hero uses HeroClass
        warrior = Hero("Ada",  hp=120, atk=15, def_=8, potions=2, gold=20,
                       hero_class=HeroClass.WARRIOR)
        mage    = Hero("Zara", hp=80,  atk=24, def_=3, potions=1, gold=30,
                       hero_class=HeroClass.MAGE)
        rogue   = Hero("Rex",  hp=100, atk=18, def_=5, potions=4, gold=15,
                       hero_class=HeroClass.ROGUE)

        assert warrior.hero_class == HeroClass.WARRIOR, \
            "warrior.hero_class should be HeroClass.WARRIOR"
        assert mage.hero_class == HeroClass.MAGE

        # class_bonus uses enum comparison, not string comparison
        assert warrior.class_bonus() == 2, \
            f"Warrior class_bonus should be 2, got {warrior.class_bonus()}"
        assert mage.class_bonus() == 0, \
            f"Mage class_bonus should be 0, got {mage.class_bonus()}"
        assert rogue.class_bonus() == 4, \
            f"Rogue class_bonus should be 4, got {rogue.class_bonus()}"

        # hero_class is NOT a plain string
        assert not isinstance(warrior.hero_class, str), \
            "hero_class should be a HeroClass enum, not a plain string"

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("05_enums")
    print("✅ Mission 05 complete: Magic strings replaced with HeroClass enum!")
    print()
    print("   Typos now raise AttributeError immediately instead of silent wrong behaviour.")
    print("   Next mission: level_2_oop_and_design/missions/06_properties/README.md")


if __name__ == "__main__":
    main()
