"""check.py — Mission 03: Load Game Catalogs"""

import json
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
PROGRESS_FILE = REPO_ROOT / "level_3_validation_and_persistence" / ".progress"


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
    task_path = Path(__file__).parent / "task.py"

    import importlib.util
    spec = importlib.util.spec_from_file_location("task", task_path)
    task = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    try:
        spec.loader.exec_module(task)  # type: ignore[union-attr]
    except Exception as e:
        print(f"❌ Could not import task.py: {e}")
        raise SystemExit(1)

    # --- MonsterConfig.to_domain ---
    MonsterConfig = getattr(task, "MonsterConfig", None)
    Monster = getattr(task, "Monster", None)
    if MonsterConfig is None or Monster is None:
        print("❌ MonsterConfig or Monster class not found in task.py.")
        raise SystemExit(1)

    try:
        cfg = MonsterConfig.model_validate({"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10})
        m = cfg.to_domain()
    except NotImplementedError:
        print("❌ MonsterConfig.to_domain() is not implemented yet.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ MonsterConfig.to_domain() raised: {e}")
        raise SystemExit(1)

    if not isinstance(m, Monster):
        print(f"❌ MonsterConfig.to_domain() must return a Monster, got {type(m).__name__}")
        raise SystemExit(1)
    if m.name != "Goblin" or m.hp != 30 or m.def_ != 2:
        print(f"❌ Monster has wrong values: {m}")
        raise SystemExit(1)

    # --- WeaponConfig.to_domain ---
    WeaponConfig = getattr(task, "WeaponConfig", None)
    Weapon = getattr(task, "Weapon", None)
    if WeaponConfig is None or Weapon is None:
        print("❌ WeaponConfig or Weapon class not found in task.py.")
        raise SystemExit(1)

    try:
        wcfg = WeaponConfig.model_validate({"name": "Iron Sword", "atk_bonus": 2, "price": 50})
        w = wcfg.to_domain()
    except NotImplementedError:
        print("❌ WeaponConfig.to_domain() is not implemented yet.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ WeaponConfig.to_domain() raised: {e}")
        raise SystemExit(1)

    if not isinstance(w, Weapon):
        print(f"❌ WeaponConfig.to_domain() must return a Weapon, got {type(w).__name__}")
        raise SystemExit(1)

    # --- load_monsters ---
    load_monsters = getattr(task, "load_monsters", None)
    if load_monsters is None:
        print("❌ load_monsters() not found in task.py.")
        raise SystemExit(1)

    try:
        monsters = load_monsters()
    except NotImplementedError:
        print("❌ load_monsters() is not implemented yet.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ load_monsters() raised: {e}")
        raise SystemExit(1)

    if len(monsters) != 4:
        print(f"❌ Expected 4 monsters from monsters.json, got {len(monsters)}")
        raise SystemExit(1)
    if not isinstance(monsters[0], Monster):
        print(f"❌ load_monsters() must return list[Monster], got {type(monsters[0])}")
        raise SystemExit(1)

    # --- load_monsters: a bad record must not kill the rest of the load ---
    mixed_monsters_data = {
        "monsters": [
            {"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10},
            {"name": "Broken", "hp": -5, "atk": 8, "def": 2, "gold": 10},  # hp <= 0
            {"name": "Orc", "hp": 50, "atk": 12, "def": 4, "gold": 20},
        ]
    }
    with tempfile.TemporaryDirectory() as tmp:
        mixed_path = Path(tmp) / "mixed_monsters.json"
        mixed_path.write_text(json.dumps(mixed_monsters_data))
        try:
            mixed_monsters = load_monsters(mixed_path)
        except NotImplementedError:
            print("❌ load_monsters() is not implemented yet.")
            raise SystemExit(1)
        except Exception as e:
            print(
                f"❌ load_monsters() must skip an invalid entry (hp=-5), not raise. "
                f"Raised {type(e).__name__}: {e}"
            )
            raise SystemExit(1)

        if len(mixed_monsters) != 2:
            print(
                f"❌ load_monsters() should skip the invalid 'Broken' entry and return "
                f"the 2 valid monsters (Goblin, Orc), got {len(mixed_monsters)}"
            )
            raise SystemExit(1)
        names = {m.name for m in mixed_monsters}
        if names != {"Goblin", "Orc"}:
            print(f"❌ load_monsters() returned the wrong monsters: {names}")
            raise SystemExit(1)
        by_name = {m.name: m for m in mixed_monsters}
        if by_name["Goblin"].hp != 30 or by_name["Orc"].hp != 50:
            print(f"❌ load_monsters() returned monsters with wrong values: {mixed_monsters}")
            raise SystemExit(1)

    # --- load_weapons ---
    load_weapons = getattr(task, "load_weapons", None)
    if load_weapons is None:
        print("❌ load_weapons() not found in task.py.")
        raise SystemExit(1)

    try:
        weapons = load_weapons()
    except NotImplementedError:
        print("❌ load_weapons() is not implemented yet.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ load_weapons() raised: {e}")
        raise SystemExit(1)

    if len(weapons) != 3:
        print(f"❌ Expected 3 weapons from weapons.json, got {len(weapons)}")
        raise SystemExit(1)
    if not isinstance(weapons[0], Weapon):
        print(f"❌ load_weapons() must return list[Weapon], got {type(weapons[0])}")
        raise SystemExit(1)

    # --- load_weapons: same graceful-skip pattern as load_monsters ---
    mixed_weapons_data = {
        "weapons": [
            {"name": "Iron Sword", "atk_bonus": 2, "price": 50},
            {"name": "Cursed Blade", "atk_bonus": -5, "price": 0},  # atk_bonus < 0
            {"name": "Bow", "atk_bonus": 3, "price": 30},
        ]
    }
    with tempfile.TemporaryDirectory() as tmp:
        mixed_wpath = Path(tmp) / "mixed_weapons.json"
        mixed_wpath.write_text(json.dumps(mixed_weapons_data))
        try:
            mixed_weapons = load_weapons(mixed_wpath)
        except NotImplementedError:
            print("❌ load_weapons() is not implemented yet.")
            raise SystemExit(1)
        except Exception as e:
            print(
                f"❌ load_weapons() must skip an invalid entry (atk_bonus=-5), not raise. "
                f"Raised {type(e).__name__}: {e}"
            )
            raise SystemExit(1)

        if len(mixed_weapons) != 2:
            print(
                f"❌ load_weapons() should skip the invalid 'Cursed Blade' entry and return "
                f"the 2 valid weapons (Iron Sword, Bow), got {len(mixed_weapons)}"
            )
            raise SystemExit(1)
        wnames = {w.name for w in mixed_weapons}
        if wnames != {"Iron Sword", "Bow"}:
            print(f"❌ load_weapons() returned the wrong weapons: {wnames}")
            raise SystemExit(1)

    print("✅ Mission 03 complete — catalogs load and convert to domain objects correctly.")
    update_progress("03_load_game_catalogs")


if __name__ == "__main__":
    main()
