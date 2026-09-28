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

        # hp_percent — several hp/max_hp pairs the README/task never show,
        # so a lookup keyed on the one example pair can't pass by accident
        percent_cases = [
            (60, 120, 50.0),
            (75, 150, 50.0),
            (17, 68, 25.0),
            (180, 200, 90.0),
            (9, 45, 20.0),
            (120, 120, 100.0),
            (0, 120, 0.0),
        ]
        for hp, max_hp, expected in percent_cases:
            c = Character("Test", hp=hp, max_hp=max_hp, atk=10, def_=5)
            assert abs(c.hp_percent - expected) < 0.01, \
                f"hp_percent should be {expected} for {hp}/{max_hp}, got {c.hp_percent}"

        # status — both sides of each threshold, exactly on each threshold,
        # and the *same* hp values as above paired with a different max_hp,
        # so a lookup like `if self.hp == 100: return "healthy"` (ignoring
        # max_hp) gets caught instead of coincidentally passing.
        status_cases = [
            (100, 120, "healthy"),   # ~83%
            (30,  120, "wounded"),   # 25%
            (10,  120, "critical"),  # ~8%
            (100, 200, "healthy"),   # exactly 50% — boundary, inclusive
            (99,  200, "wounded"),   # just under 50%
            (40,  200, "wounded"),   # exactly 20% — boundary, inclusive
            (39,  200, "critical"),  # just under 20%
            (45,  50,  "healthy"),   # 90%, values never used above
            (100, 1000, "critical"), # same hp=100 as the first case, different max_hp
            (30,  30,  "healthy"),   # same hp=30 as the first case, different max_hp
            (10,  10,  "healthy"),   # same hp=10 as the first case, different max_hp
        ]
        for hp, max_hp, expected in status_cases:
            c = Character("Test", hp=hp, max_hp=max_hp, atk=10, def_=5)
            assert c.status == expected, \
                f"status for hp={hp}/{max_hp} should be '{expected}', got '{c.status}'"

        # Properties are read-only
        probe = Character("Probe", hp=100, max_hp=120, atk=10, def_=5)
        try:
            probe.is_alive = False
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
