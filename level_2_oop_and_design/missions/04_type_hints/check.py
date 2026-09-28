"""check.py — Mission 04: Type Hints"""

import json
from pathlib import Path
from typing import get_type_hints

REPO_ROOT = Path(__file__).parents[3]
PROGRESS_FILE = REPO_ROOT / "level_2_oop_and_design" / ".progress"

NONE_TYPE = type(None)


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


def _hints(fn: object, label: str) -> dict:
    """Resolve real type objects (not strings) via typing.get_type_hints,
    so `hp: "int"` and `hp: int` are treated the same, and a placeholder
    like `hp: object` is caught instead of just checking a hint exists."""
    try:
        return get_type_hints(fn)
    except Exception as e:
        raise AssertionError(f"Could not resolve type hints for {label}: {e}")


def _check(hints: dict, name: str, expected: type, label: str) -> None:
    assert name in hints, f"{label} is missing a type hint for '{name}'"
    actual = hints[name]
    assert actual is expected, (
        f"{label}: '{name}' should be annotated as {expected.__name__}, "
        f"got {getattr(actual, '__name__', actual)!r} — a hint has to name "
        f"the real type, not a placeholder like 'object'"
    )


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
        # Character.__init__
        hints = _hints(Character.__init__, "Character.__init__")
        _check(hints, "name", str, "Character.__init__")
        _check(hints, "hp", int, "Character.__init__")
        _check(hints, "atk", int, "Character.__init__")
        _check(hints, "def_", int, "Character.__init__")
        _check(hints, "return", NONE_TYPE, "Character.__init__")

        # Character.is_alive
        hints = _hints(Character.is_alive, "Character.is_alive")
        _check(hints, "return", bool, "Character.is_alive")

        # Character.take_damage
        hints = _hints(Character.take_damage, "Character.take_damage")
        _check(hints, "amount", int, "Character.take_damage")
        _check(hints, "return", NONE_TYPE, "Character.take_damage")

        # Hero.__init__
        hints = _hints(Hero.__init__, "Hero.__init__")
        _check(hints, "name", str, "Hero.__init__")
        _check(hints, "hp", int, "Hero.__init__")
        _check(hints, "atk", int, "Hero.__init__")
        _check(hints, "def_", int, "Hero.__init__")
        _check(hints, "potions", int, "Hero.__init__")
        _check(hints, "gold", int, "Hero.__init__")
        _check(hints, "return", NONE_TYPE, "Hero.__init__")

        # Hero.use_potion
        hints = _hints(Hero.use_potion, "Hero.use_potion")
        _check(hints, "heal_amount", int, "Hero.use_potion")
        _check(hints, "return", bool, "Hero.use_potion")

        # Monster.__init__
        hints = _hints(Monster.__init__, "Monster.__init__")
        _check(hints, "name", str, "Monster.__init__")
        _check(hints, "hp", int, "Monster.__init__")
        _check(hints, "atk", int, "Monster.__init__")
        _check(hints, "def_", int, "Monster.__init__")
        _check(hints, "gold", int, "Monster.__init__")
        _check(hints, "return", NONE_TYPE, "Monster.__init__")

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
