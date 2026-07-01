"""check.py — Mission 04: Type Hints"""

import json
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


def has_annotations(fn: object) -> bool:
    hints = getattr(fn, "__annotations__", {})
    return bool(hints)


def main() -> None:
    try:
        from task import Character, Hero, Monster
    except ImportError as e:
        print(f"❌ Could not import from task.py: {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error in task.py: {e}")
        raise SystemExit(1)

    try:
        # Check that __init__ methods have annotations
        for cls, name in [(Character, "Character"), (Hero, "Hero"), (Monster, "Monster")]:
            init = cls.__init__
            hints = init.__annotations__
            assert hints, f"{name}.__init__ has no type annotations — add them to all parameters"
            assert "return" in hints, \
                f"{name}.__init__ is missing '-> None' return annotation"

        # Check is_alive and take_damage
        for cls, name in [(Character, "Character")]:
            is_alive = cls.is_alive
            hints = is_alive.__annotations__
            assert "return" in hints, \
                f"{name}.is_alive() is missing a return type annotation"

            take_dmg = cls.take_damage
            hints = take_dmg.__annotations__
            assert hints, f"{name}.take_damage() has no annotations"
            assert "return" in hints, \
                f"{name}.take_damage() is missing '-> None' return annotation"

        # Runtime behaviour still works
        h = Hero("Ada", hp=120, atk=15, def_=8, potions=2, gold=20)
        m = Monster("Goblin", hp=30, atk=8, def_=2, gold=10)
        assert h.is_alive() is True
        m.take_damage(30)
        assert m.is_alive() is False

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("04_type_hints")
    print("✅ Mission 04 complete: All methods and attributes are annotated!")
    print()
    print("   Type hints make contracts explicit and enable editor autocomplete.")
    print("   Next mission: level_2_oop_and_design/missions/05_enums/README.md")


if __name__ == "__main__":
    main()
