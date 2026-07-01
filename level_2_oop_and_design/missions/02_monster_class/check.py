"""check.py — Mission 02: Monster Class"""

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
        from task import Monster, goblin, orc, dragon
    except ImportError as e:
        print(f"❌ Could not import from task.py: {e}")
        print("   Make sure you defined 'class Monster' and created goblin, orc, dragon.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error in task.py: {e}")
        raise SystemExit(1)

    try:
        # Basic attributes
        assert isinstance(goblin, Monster), f"goblin should be a Monster, got {type(goblin)}"
        assert goblin.name == "Goblin", f"goblin.name should be 'Goblin', got '{goblin.name}'"
        assert goblin.hp == 30, f"goblin.hp should be 30, got {goblin.hp}"
        assert goblin.atk == 8, f"goblin.atk should be 8, got {goblin.atk}"
        assert goblin.def_ == 2, f"goblin.def_ should be 2, got {goblin.def_}"
        assert goblin.gold == 10, f"goblin.gold should be 10, got {goblin.gold}"

        assert orc.name == "Orc" and orc.hp == 55
        assert dragon.name == "Dragon" and dragon.hp == 120

        # is_alive method
        assert goblin.is_alive() is True, "goblin.is_alive() should be True (hp=30)"

        alive_m = Monster("Alive", 1, 5, 1, 0)
        dead_m  = Monster("Dead",  0, 5, 1, 0)
        assert alive_m.is_alive() is True,  "Monster with hp=1 should be alive"
        assert dead_m.is_alive()  is False, "Monster with hp=0 should not be alive"

        # take_damage method
        test_m = Monster("Test", 30, 8, 2, 5)
        test_m.take_damage(10)
        assert test_m.hp == 20, f"After 10 damage from 30 hp, should have 20, got {test_m.hp}"

        test_m.take_damage(100)
        assert test_m.hp == 0, f"HP should not go below 0, got {test_m.hp}"

        assert not test_m.is_alive(), "Monster with hp=0 should not be alive after take_damage"

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("02_monster_class")
    print("✅ Mission 02 complete: Monster is now a proper class with methods!")
    print()
    print("   Monsters have data (attributes) AND behaviour (methods) in one place.")
    print("   Next mission: level_2_oop_and_design/missions/03_character_base/README.md")


if __name__ == "__main__":
    main()
