"""check.py — Mission 07: Settings and Paths"""

import json
import os
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

    GameSettings = getattr(task, "GameSettings", None)
    get_settings = getattr(task, "get_settings", None)

    if GameSettings is None:
        print("❌ GameSettings not found in task.py.")
        raise SystemExit(1)
    if get_settings is None:
        print("❌ get_settings() not found in task.py.")
        raise SystemExit(1)

    # Basic construction
    try:
        settings = get_settings()
    except Exception as e:
        print(f"❌ get_settings() raised: {e}")
        raise SystemExit(1)

    # Check required fields
    for field_name in ("data_dir", "saves_dir", "log_file", "max_potions"):
        if not hasattr(settings, field_name):
            print(f"❌ GameSettings is missing field '{field_name}'.")
            raise SystemExit(1)

    if not isinstance(settings.data_dir, Path):
        print(f"❌ data_dir must be a Path, got {type(settings.data_dir).__name__}")
        raise SystemExit(1)
    if not isinstance(settings.saves_dir, Path):
        print(f"❌ saves_dir must be a Path, got {type(settings.saves_dir).__name__}")
        raise SystemExit(1)
    if not isinstance(settings.max_potions, int):
        print(f"❌ max_potions must be int, got {type(settings.max_potions).__name__}")
        raise SystemExit(1)
    if settings.max_potions <= 0:
        print(f"❌ max_potions must be > 0, got {settings.max_potions}")
        raise SystemExit(1)

    # get_settings() should return the same instance (caching)
    settings2 = get_settings()
    if settings is not settings2:
        print("❌ get_settings() should return the same instance on repeated calls (caching).")
        raise SystemExit(1)

    # Environment variable override (only if BaseSettings is used)
    env_override_supported = True
    try:
        import pydantic_settings  # noqa: F401
    except ImportError:
        env_override_supported = False

    if env_override_supported:
        # Reset the cache so a fresh instance is created with the env var
        if hasattr(task, "_settings"):
            task._settings = None

        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["RPG_SAVES_DIR"] = tmp
            try:
                overridden = GameSettings()  # type: ignore[call-arg]
                if str(overridden.saves_dir) != tmp:
                    print(
                        f"❌ RPG_SAVES_DIR env var should override saves_dir. "
                        f"Expected {tmp}, got {overridden.saves_dir}"
                    )
                    raise SystemExit(1)
            except Exception as e:
                print(f"❌ GameSettings() with env var raised: {e}")
                raise SystemExit(1)
            finally:
                del os.environ["RPG_SAVES_DIR"]
                if hasattr(task, "_settings"):
                    task._settings = None

    print("✅ Mission 07 complete — GameSettings is defined and get_settings() caches correctly.")
    if env_override_supported:
        print("   (pydantic-settings detected — env var override also verified.)")
    else:
        print("   (pydantic-settings not installed — env var override skipped.)")
    update_progress("07_settings_and_paths")


if __name__ == "__main__":
    main()
