"""check.py — Mission 03: Load Game Catalogs"""

import json
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

    print("✅ Mission 03 complete — catalogs load and convert to domain objects correctly.")
    update_progress("03_load_game_catalogs")


if __name__ == "__main__":
    main()
