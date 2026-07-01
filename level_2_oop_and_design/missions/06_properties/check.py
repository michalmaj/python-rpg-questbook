"""check.py — Mission 06: Properties"""

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


def main() -> None:
    try:
        from task import Character
    except ImportError as e:
        print(f"❌ Could not import from task.py: {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error in task.py: {e}")
        raise SystemExit(1)

    try:
        # Check properties exist and are properties (not plain methods)
        for prop_name in ("is_alive", "hp_percent", "status"):
            assert isinstance(getattr(Character, prop_name), property), \
                f"'{prop_name}' should be a @property, not a regular method"

        # is_alive
        c = Character("Test", hp=100, max_hp=100, atk=10, def_=5)
        assert c.is_alive is True, "is_alive should be True when hp=100"
        c.take_damage(100)
        assert c.is_alive is False, "is_alive should be False when hp=0"

        # hp_percent
        c2 = Character("Test2", hp=60, max_hp=120, atk=10, def_=5)
        assert abs(c2.hp_percent - 50.0) < 0.01, \
            f"hp_percent should be 50.0 for 60/120, got {c2.hp_percent}"

        c3 = Character("Test3", hp=120, max_hp=120, atk=10, def_=5)
        assert abs(c3.hp_percent - 100.0) < 0.01, \
            f"hp_percent should be 100.0 for 120/120, got {c3.hp_percent}"

        c4 = Character("Test4", hp=0, max_hp=120, atk=10, def_=5)
        assert abs(c4.hp_percent - 0.0) < 0.01, \
            f"hp_percent should be 0.0 for 0/120, got {c4.hp_percent}"

        # status
        healthy  = Character("H", hp=100, max_hp=120, atk=10, def_=5)
        wounded  = Character("W", hp=30,  max_hp=120, atk=10, def_=5)
        critical = Character("C", hp=10,  max_hp=120, atk=10, def_=5)

        assert healthy.status  == "healthy",  f"Expected 'healthy', got '{healthy.status}'"
        assert wounded.status  == "wounded",  f"Expected 'wounded', got '{wounded.status}'"
        assert critical.status == "critical", f"Expected 'critical', got '{critical.status}'"

        # Properties are read-only
        try:
            healthy.is_alive = False
            print("❌ is_alive should be read-only (no setter)")
            raise SystemExit(1)
        except AttributeError:
            pass  # correct — properties without a setter raise AttributeError on assignment

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("06_properties")
    print("✅ Mission 06 complete: Character has is_alive, hp_percent, and status properties!")
    print()
    print("   'hero.is_alive' reads like plain English. That is the point of properties.")
    print("   Next mission: level_2_oop_and_design/missions/07_dataclasses/README.md")


if __name__ == "__main__":
    main()
