"""check.py — Mission 07: Dataclasses"""

import dataclasses
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
        from task import MonsterTemplate, goblin_template, orc_template, troll_template, dragon_template
    except ImportError as e:
        print(f"❌ Could not import from task.py: {e}")
        print("   Make sure MonsterTemplate is a @dataclass and all four templates are created.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error in task.py: {e}")
        raise SystemExit(1)

    try:
        # Is it a dataclass?
        assert dataclasses.is_dataclass(MonsterTemplate), \
            "MonsterTemplate should be decorated with @dataclass"

        # Fields check
        fields = {f.name for f in dataclasses.fields(MonsterTemplate)}
        assert "name"  in fields, "MonsterTemplate should have a 'name' field"
        assert "hp"    in fields, "MonsterTemplate should have a 'hp' field"
        assert "atk"   in fields, "MonsterTemplate should have an 'atk' field"
        assert "def_"  in fields, "MonsterTemplate should have a 'def_' field"
        assert "gold"  in fields, "MonsterTemplate should have a 'gold' field"

        # Correct values
        assert goblin_template.name == "Goblin" and goblin_template.hp == 30, \
            f"goblin_template values wrong: {goblin_template}"
        assert orc_template.name == "Orc" and orc_template.hp == 55
        assert troll_template.name == "Troll" and troll_template.hp == 80
        assert dragon_template.name == "Dragon" and dragon_template.hp == 120

        # __repr__ generated — should contain class name and field values
        r = repr(goblin_template)
        assert "MonsterTemplate" in r and "Goblin" in r, \
            f"__repr__ should include class name and field values, got: {r}"

        # __eq__ generated
        goblin2 = MonsterTemplate(name="Goblin", hp=30, atk=8, def_=2, gold=10)
        assert goblin_template == goblin2, \
            "Two MonsterTemplates with equal fields should compare as equal"
        assert goblin_template != orc_template, \
            "Different monsters should not be equal"

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("07_dataclasses")
    print("✅ Mission 07 complete: MonsterTemplate is now a @dataclass!")
    print()
    print("   __init__, __repr__, and __eq__ were generated automatically.")
    print("   Next mission: level_2_oop_and_design/missions/08_module_split/README.md")


if __name__ == "__main__":
    main()
