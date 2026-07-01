"""check.py — Mission 02: Pydantic Monster Config"""

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

    # Check MonsterConfig exists
    MonsterConfig = getattr(task, "MonsterConfig", None)
    if MonsterConfig is None:
        print("❌ MonsterConfig not found in task.py.")
        raise SystemExit(1)

    # Check WeaponConfig exists
    WeaponConfig = getattr(task, "WeaponConfig", None)
    if WeaponConfig is None:
        print("❌ WeaponConfig not found in task.py.")
        raise SystemExit(1)

    # MonsterConfig — valid goblin via alias
    try:
        m = MonsterConfig.model_validate({"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10})
    except Exception as e:
        print(f"❌ MonsterConfig rejected a valid Goblin: {e}")
        raise SystemExit(1)

    if m.hp != 30:
        print(f"❌ MonsterConfig.hp should be 30, got {m.hp}")
        raise SystemExit(1)
    if m.def_ != 2:
        print(f"❌ MonsterConfig.def_ should be 2, got {m.def_!r} (check alias='def')")
        raise SystemExit(1)

    # MonsterConfig — negative hp must fail
    try:
        MonsterConfig.model_validate({"name": "Ghost", "hp": -50, "atk": 8, "def": 2, "gold": 15})
        print("❌ MonsterConfig accepted hp=-50 — Field(gt=0) is missing.")
        raise SystemExit(1)
    except Exception:
        pass

    # MonsterConfig — missing hp must fail
    try:
        MonsterConfig.model_validate({"name": "Bandit", "atk": 10, "def": 3, "gold": 20})
        print("❌ MonsterConfig accepted a monster with no 'hp' field.")
        raise SystemExit(1)
    except Exception:
        pass

    # WeaponConfig — valid
    try:
        w = WeaponConfig.model_validate({"name": "Iron Sword", "atk_bonus": 2, "price": 50})
    except Exception as e:
        print(f"❌ WeaponConfig rejected a valid weapon: {e}")
        raise SystemExit(1)

    if w.atk_bonus != 2:
        print(f"❌ WeaponConfig.atk_bonus should be 2, got {w.atk_bonus}")
        raise SystemExit(1)

    # WeaponConfig — negative atk_bonus must fail
    try:
        WeaponConfig.model_validate({"name": "Cursed Blade", "atk_bonus": -5, "price": 0})
        print("❌ WeaponConfig accepted atk_bonus=-5 — Field(ge=0) is missing.")
        raise SystemExit(1)
    except Exception:
        pass

    print("✅ Mission 02 complete — MonsterConfig and WeaponConfig validate correctly.")
    update_progress("02_pydantic_monster_config")


if __name__ == "__main__":
    main()
