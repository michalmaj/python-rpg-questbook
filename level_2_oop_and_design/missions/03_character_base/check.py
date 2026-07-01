"""check.py — Mission 03: Character Base"""

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
        from task import Character, Hero, Monster
    except ImportError as e:
        print(f"❌ Could not import from task.py: {e}")
        print("   Make sure you defined Character, Hero, and Monster.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error in task.py: {e}")
        raise SystemExit(1)

    try:
        # Character base class
        c = Character("Test", hp=50, atk=10, def_=5)
        assert c.name == "Test"
        assert c.hp == 50
        assert c.is_alive() is True
        c.take_damage(50)
        assert c.hp == 0
        assert c.is_alive() is False
        c.take_damage(100)
        assert c.hp == 0, "HP should never go below 0"

        # Hero inherits from Character
        assert issubclass(Hero, Character), "Hero should inherit from Character"
        h = Hero("Ada", hp=120, atk=15, def_=8, potions=2, gold=20)
        assert h.name == "Ada"
        assert h.hp == 120
        assert h.potions == 2
        assert h.gold == 20
        assert h.is_alive() is True        # inherited method
        h.take_damage(30)
        assert h.hp == 90                  # inherited method

        # Monster inherits from Character
        assert issubclass(Monster, Character), "Monster should inherit from Character"
        m = Monster("Goblin", hp=30, atk=8, def_=2, gold=10)
        assert m.name == "Goblin"
        assert m.hp == 30
        assert m.gold == 10
        assert m.is_alive() is True
        m.take_damage(30)
        assert m.is_alive() is False

        # Both use the same inherited methods
        for obj in [h, m]:
            assert hasattr(obj, "is_alive"),    f"{type(obj).__name__} should have is_alive()"
            assert hasattr(obj, "take_damage"), f"{type(obj).__name__} should have take_damage()"

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("03_character_base")
    print("✅ Mission 03 complete: Hero and Monster share a Character base class!")
    print()
    print("   Duplicated logic now lives in one place. One change fixes both classes.")
    print("   Next mission: level_2_oop_and_design/missions/04_type_hints/README.md")


if __name__ == "__main__":
    main()
