"""check.py — Mission 01: External Data Is Untrusted"""

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


def _has_field_error(errors: list, field: str) -> bool:
    return any(field.lower() in e.lower() for e in errors)


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

    fn = getattr(task, "validate_monster", None)
    if fn is None:
        print("❌ validate_monster() not found in task.py.")
        raise SystemExit(1)

    # --- valid monster: no errors ---
    valid = {"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10}
    errors = fn(valid)
    if errors:
        print(f"❌ Valid Goblin should produce no errors, got: {errors}")
        raise SystemExit(1)

    # --- hp: negative ---
    errors = fn({"name": "Ghost", "hp": -50, "atk": 8, "def": 2, "gold": 15})
    if not _has_field_error(errors, "hp"):
        print("❌ hp=-50 was not caught (expected an hp error).")
        raise SystemExit(1)

    # --- hp: wrong type (str) ---
    errors = fn({"name": "Slime", "hp": "lots", "atk": 5, "def": 1, "gold": 5})
    if not _has_field_error(errors, "hp"):
        print('❌ hp="lots" (str) was not caught (expected an hp error).')
        raise SystemExit(1)

    # --- hp: missing ---
    errors = fn({"name": "Bandit", "atk": 10, "def": 3, "gold": 20})
    if not _has_field_error(errors, "hp"):
        print("❌ Missing 'hp' was not caught (expected an hp error).")
        raise SystemExit(1)

    # --- name: missing ---
    errors = fn({"hp": 30, "atk": 8, "def": 2, "gold": 10})
    if not _has_field_error(errors, "name"):
        print("❌ Missing 'name' was not caught (expected a name error).")
        raise SystemExit(1)

    # --- name: wrong type (int) ---
    errors = fn({"name": 42, "hp": 30, "atk": 8, "def": 2, "gold": 10})
    if not _has_field_error(errors, "name"):
        print("❌ name=42 (int) was not caught (expected a name error).")
        raise SystemExit(1)

    # --- atk: zero (must be >= 1) ---
    errors = fn({"name": "Weak", "hp": 10, "atk": 0, "def": 2, "gold": 5})
    if not _has_field_error(errors, "atk"):
        print("❌ atk=0 was not caught (expected an atk error; atk must be >= 1).")
        raise SystemExit(1)

    # --- gold: negative ---
    errors = fn({"name": "Thief", "hp": 20, "atk": 5, "def": 1, "gold": -10})
    if not _has_field_error(errors, "gold"):
        print("❌ gold=-10 was not caught (expected a gold error).")
        raise SystemExit(1)

    # --- extra field: should still be valid ---
    errors = fn({"name": "Ogre", "hp": 60, "atk": 14, "def": 5, "gold": 30, "secret_power": "fire"})
    if errors:
        print(f"❌ Monster with unknown extra field should be valid. Got: {errors}")
        raise SystemExit(1)

    print("✅ Mission 01 complete — validate_monster() catches all required problems.")
    update_progress("01_external_data_is_untrusted")


if __name__ == "__main__":
    main()
