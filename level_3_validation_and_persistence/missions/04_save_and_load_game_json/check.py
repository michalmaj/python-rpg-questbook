"""check.py — Mission 04: Save and Load Game JSON"""

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

    SaveGameModel = getattr(task, "SaveGameModel", None)
    Hero = getattr(task, "Hero", None)
    HeroClass = getattr(task, "HeroClass", None)
    save_game = getattr(task, "save_game", None)
    load_game = getattr(task, "load_game", None)

    for name, obj in [("SaveGameModel", SaveGameModel), ("Hero", Hero),
                      ("HeroClass", HeroClass), ("save_game", save_game), ("load_game", load_game)]:
        if obj is None:
            print(f"❌ {name} not found in task.py.")
            raise SystemExit(1)

    hero = Hero(
        name="Ada",
        hero_class=HeroClass.WARRIOR,
        hp=100,
        max_hp=120,
        atk=12,
        def_=4,
        potions=2,
        gold=55,
        wins=3,
        losses=1,
    )

    with tempfile.TemporaryDirectory() as tmp:
        save_path = Path(tmp) / "save_game.json"

        # --- save ---
        try:
            save_game(hero, save_path)
        except NotImplementedError:
            print("❌ save_game() is not implemented yet.")
            raise SystemExit(1)
        except Exception as e:
            print(f"❌ save_game() raised: {e}")
            raise SystemExit(1)

        if not save_path.exists():
            print("❌ save_game() did not create the save file.")
            raise SystemExit(1)

        raw = json.loads(save_path.read_text())
        if "schema_version" not in raw:
            print("❌ Save file is missing 'schema_version' field.")
            raise SystemExit(1)
        if raw["schema_version"] != 1:
            print(f"❌ schema_version should be 1, got {raw['schema_version']}")
            raise SystemExit(1)

        # --- load ---
        try:
            loaded = load_game(save_path)
        except NotImplementedError:
            print("❌ load_game() is not implemented yet.")
            raise SystemExit(1)
        except Exception as e:
            print(f"❌ load_game() raised: {e}")
            raise SystemExit(1)

        if loaded is None:
            print("❌ load_game() returned None even though the save file exists.")
            raise SystemExit(1)
        if not isinstance(loaded, Hero):
            print(f"❌ load_game() must return a Hero, got {type(loaded).__name__}")
            raise SystemExit(1)
        if loaded.name != "Ada" or loaded.hp != 100 or loaded.gold != 55:
            print(f"❌ Loaded hero has wrong values: name={loaded.name}, hp={loaded.hp}, gold={loaded.gold}")
            raise SystemExit(1)
        if loaded.hero_class != HeroClass.WARRIOR:
            print(f"❌ Loaded hero class should be WARRIOR, got {loaded.hero_class}")
            raise SystemExit(1)

        # --- load from non-existent file ---
        missing = Path(tmp) / "no_save.json"
        result = load_game(missing)
        if result is not None:
            print("❌ load_game() should return None when the file does not exist.")
            raise SystemExit(1)

        # --- schema version mismatch ---
        raw["schema_version"] = 99
        save_path.write_text(json.dumps(raw))
        try:
            load_game(save_path)
            print("❌ load_game() should raise ValueError when schema_version does not match.")
            raise SystemExit(1)
        except ValueError:
            pass  # expected
        except NotImplementedError:
            print("❌ load_game() schema_version check is not implemented yet.")
            raise SystemExit(1)
        except Exception as e:
            print(f"❌ Expected ValueError for version mismatch, got {type(e).__name__}: {e}")
            raise SystemExit(1)

    print("✅ Mission 04 complete — save_game and load_game work with schema_version.")
    update_progress("04_save_and_load_game_json")


if __name__ == "__main__":
    main()
