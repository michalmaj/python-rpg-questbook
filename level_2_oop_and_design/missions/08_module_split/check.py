"""check.py — Mission 08: Module Split"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
MISSION_DIR = Path(__file__).parent
PROGRESS_FILE = REPO_ROOT / "level_2_oop_and_design" / ".progress"

sys.path.insert(0, str(MISSION_DIR))


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
        from rpg.hero import Hero, HeroClass
        from rpg.monster import Monster, MonsterTemplate
        from rpg.combat import compute_damage, hero_turn, monster_turn
    except ImportError as e:
        print(f"❌ Could not import from the rpg/ package: {e}")
        print("   Make sure rpg/__init__.py exists and rpg/combat.py is complete.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error importing rpg package: {e}")
        raise SystemExit(1)

    try:
        # compute_damage
        dmg = compute_damage(15, 5)
        assert isinstance(dmg, int), f"compute_damage should return int, got {type(dmg)}"
        assert dmg >= 1, "compute_damage should return at least 1"

        # Minimum 1
        dmg_floored = compute_damage(1, 100)
        assert dmg_floored == 1, f"compute_damage with atk=1, def=100 should return 1, got {dmg_floored}"

        # hero_turn and monster_turn
        hero = Hero("Ada", HeroClass.WARRIOR, hp=120, max_hp=120, atk=15, def_=8, potions=2, gold=20)
        tmpl = MonsterTemplate("Goblin", hp=30, atk=8, def_=2, gold=10)
        monster = Monster(tmpl)

        result = hero_turn(hero, monster)
        assert isinstance(result, tuple) and len(result) == 2, \
            "hero_turn should return a (damage, is_crit) tuple"
        dmg, is_crit = result
        assert isinstance(dmg, int) and dmg >= 1, f"hero_turn damage should be int >= 1, got {dmg}"
        assert isinstance(is_crit, bool), f"hero_turn is_crit should be bool, got {type(is_crit)}"
        assert monster.hp < 30, "hero_turn should have called monster.take_damage()"

        hero2 = Hero("Ada", HeroClass.WARRIOR, hp=120, max_hp=120, atk=15, def_=8, potions=2, gold=20)
        monster2 = Monster(tmpl)
        result2 = monster_turn(monster2, hero2)
        assert isinstance(result2, tuple) and len(result2) == 2, \
            "monster_turn should return a (damage, is_crit) tuple"
        dmg2, is_crit2 = result2
        assert isinstance(dmg2, int) and dmg2 >= 1
        assert hero2.hp < 120, "monster_turn should have called hero.take_damage()"

        # Package structure
        assert (MISSION_DIR / "rpg" / "__init__.py").exists(), \
            "rpg/__init__.py is missing — the package needs it"
        assert (MISSION_DIR / "rpg" / "hero.py").exists()
        assert (MISSION_DIR / "rpg" / "monster.py").exists()
        assert (MISSION_DIR / "rpg" / "combat.py").exists()

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("08_module_split")
    print("✅ Mission 08 complete: The RPG is split into a proper package!")
    print()
    print("   hero.py, monster.py, combat.py — each file has one job.")
    print("   Next mission: level_2_oop_and_design/missions/09_pure_functions/README.md")


if __name__ == "__main__":
    main()
