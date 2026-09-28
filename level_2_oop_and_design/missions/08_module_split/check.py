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
        # compute_damage — sample many times per (atk, def_) pair and check
        # the whole *range* of outcomes, not just one call. This is what
        # catches a stub like `return 1`: it can't reproduce a range at all.
        def damage_range(atk, def_, samples=200):
            results = {compute_damage(atk, def_) for _ in range(samples)}
            assert all(isinstance(r, int) for r in results), \
                f"compute_damage should always return int, got {results}"
            return results

        base = damage_range(15, 5)  # atk + roll(6) - def_ = 15 + [1..6] - 5 = 11..16
        assert base and base <= set(range(11, 17)), \
            f"compute_damage(15, 5) should only produce values 11-16, got {sorted(base)}"
        assert len(base) > 1, \
            "compute_damage(15, 5) returned the same value on every call — it should vary with the d6 roll"

        higher_atk = damage_range(25, 5)  # 21..26
        assert higher_atk and higher_atk <= set(range(21, 27)), (
            "compute_damage(25, 5) should only produce values 21-26 — "
            f"attack should raise damage over compute_damage(15, 5), got {sorted(higher_atk)}"
        )

        higher_def = damage_range(15, 12)  # 4..9
        assert higher_def and higher_def <= set(range(4, 10)), (
            "compute_damage(15, 12) should only produce values 4-9 — "
            f"defence should lower damage compared to compute_damage(15, 5), got {sorted(higher_def)}"
        )

        # Minimum 1 — always, not just once
        dmg_floored = compute_damage(1, 100)
        assert dmg_floored == 1, f"compute_damage with atk=1, def=100 should return 1, got {dmg_floored}"
        floored_range = damage_range(1, 100, samples=20)
        assert floored_range == {1}, \
            f"compute_damage(1, 100) should always floor to 1, got {sorted(floored_range)}"

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
