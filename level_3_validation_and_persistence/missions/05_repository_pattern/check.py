"""check.py — Mission 05: Repository Pattern"""

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

    Hero = getattr(task, "Hero", None)
    HeroClass = getattr(task, "HeroClass", None)
    JsonSaveRepository = getattr(task, "JsonSaveRepository", None)
    InMemorySaveRepository = getattr(task, "InMemorySaveRepository", None)

    for name, obj in [("Hero", Hero), ("HeroClass", HeroClass),
                      ("JsonSaveRepository", JsonSaveRepository),
                      ("InMemorySaveRepository", InMemorySaveRepository)]:
        if obj is None:
            print(f"❌ {name} not found in task.py.")
            raise SystemExit(1)

    hero = Hero(
        name="Turing",
        hero_class=HeroClass.MAGE,
        hp=80,
        max_hp=80,
        atk=18,
        def_=2,
        potions=3,
        gold=100,
        wins=5,
        losses=0,
    )

    # --- JsonSaveRepository ---
    with tempfile.TemporaryDirectory() as tmp:
        save_path = Path(tmp) / "save_game.json"
        repo = JsonSaveRepository(save_path)

        try:
            repo.save(hero)
        except NotImplementedError:
            print("❌ JsonSaveRepository.save() is not implemented yet.")
            raise SystemExit(1)
        except Exception as e:
            print(f"❌ JsonSaveRepository.save() raised: {e}")
            raise SystemExit(1)

        if not save_path.exists():
            print("❌ JsonSaveRepository.save() did not create the file.")
            raise SystemExit(1)

        try:
            loaded = repo.load()
        except NotImplementedError:
            print("❌ JsonSaveRepository.load() is not implemented yet.")
            raise SystemExit(1)
        except Exception as e:
            print(f"❌ JsonSaveRepository.load() raised: {e}")
            raise SystemExit(1)

        if loaded is None:
            print("❌ JsonSaveRepository.load() returned None after saving.")
            raise SystemExit(1)
        if loaded.name != "Turing" or loaded.gold != 100:
            print(f"❌ Loaded hero has wrong data: {loaded}")
            raise SystemExit(1)

        # load from missing file → None
        missing_repo = JsonSaveRepository(Path(tmp) / "missing.json")
        result = missing_repo.load()
        if result is not None:
            print("❌ JsonSaveRepository.load() should return None when file is missing.")
            raise SystemExit(1)

    # --- InMemorySaveRepository ---
    mem_repo = InMemorySaveRepository()

    try:
        result = mem_repo.load()
    except NotImplementedError:
        print("❌ InMemorySaveRepository.load() is not implemented yet.")
        raise SystemExit(1)
    if result is not None:
        print("❌ InMemorySaveRepository.load() should return None before any save.")
        raise SystemExit(1)

    try:
        mem_repo.save(hero)
    except NotImplementedError:
        print("❌ InMemorySaveRepository.save() is not implemented yet.")
        raise SystemExit(1)

    loaded_mem = mem_repo.load()
    if loaded_mem is None:
        print("❌ InMemorySaveRepository.load() returned None after saving.")
        raise SystemExit(1)
    if loaded_mem.name != "Turing":
        print(f"❌ InMemorySaveRepository loaded wrong hero: {loaded_mem.name}")
        raise SystemExit(1)

    print("✅ Mission 05 complete — JsonSaveRepository and InMemorySaveRepository work correctly.")
    update_progress("05_repository_pattern")


if __name__ == "__main__":
    main()
