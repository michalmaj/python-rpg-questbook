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


def _should_fail(model_cls, data: dict, label: str) -> None:
    """Assert that model_cls.model_validate(data) raises an exception."""
    try:
        model_cls.model_validate(data)
        print(f"❌ {label}: expected ValidationError, but validation passed.")
        raise SystemExit(1)
    except SystemExit:
        raise
    except Exception:
        pass  # expected


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

    MonsterConfig = getattr(task, "MonsterConfig", None)
    WeaponConfig = getattr(task, "WeaponConfig", None)

    for name, obj in [("MonsterConfig", MonsterConfig), ("WeaponConfig", WeaponConfig)]:
        if obj is None:
            print(f"❌ {name} not found in task.py.")
            raise SystemExit(1)

    # ── MonsterConfig: valid monster via "def" alias ───────────────────────────
    try:
        m = MonsterConfig.model_validate({"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10})
    except Exception as e:
        print(f"❌ MonsterConfig rejected a valid Goblin: {e}")
        raise SystemExit(1)

    if m.hp != 30:
        print(f"❌ MonsterConfig.hp should be 30, got {m.hp}")
        raise SystemExit(1)
    if m.def_ != 2:
        print(f"❌ MonsterConfig.def_ should be 2, got {m.def_!r} — check alias='def'")
        raise SystemExit(1)
    if m.atk != 8:
        print(f"❌ MonsterConfig.atk should be 8, got {m.atk}")
        raise SystemExit(1)
    if m.gold != 10:
        print(f"❌ MonsterConfig.gold should be 10, got {m.gold}")
        raise SystemExit(1)

    # ── MonsterConfig: must reject invalid data ────────────────────────────────
    _should_fail(MonsterConfig,
                 {"name": "Ghost", "hp": -50, "atk": 8, "def": 2, "gold": 15},
                 "hp=-50 (Field gt=0 missing)")
    _should_fail(MonsterConfig,
                 {"name": "Slime", "hp": 0, "atk": 5, "def": 1, "gold": 5},
                 "hp=0 (Field gt=0 missing)")
    _should_fail(MonsterConfig,
                 {"name": "Bandit", "atk": 10, "def": 3, "gold": 20},
                 "hp missing")
    _should_fail(MonsterConfig,
                 {"name": "Weakling", "hp": 10, "atk": 0, "def": 0, "gold": 0},
                 "atk=0 (Field ge=1 missing)")
    _should_fail(MonsterConfig,
                 {"name": "Thief", "hp": 20, "atk": 5, "def": 0, "gold": -1},
                 "gold=-1 (Field ge=0 missing)")

    # ── WeaponConfig: valid weapon ─────────────────────────────────────────────
    try:
        w = WeaponConfig.model_validate({"name": "Iron Sword", "atk_bonus": 2, "price": 50})
    except Exception as e:
        print(f"❌ WeaponConfig rejected a valid weapon: {e}")
        raise SystemExit(1)

    if w.atk_bonus != 2:
        print(f"❌ WeaponConfig.atk_bonus should be 2, got {w.atk_bonus}")
        raise SystemExit(1)
    if w.price != 50:
        print(f"❌ WeaponConfig.price should be 50, got {w.price}")
        raise SystemExit(1)

    # ── WeaponConfig: must reject invalid data ─────────────────────────────────
    _should_fail(WeaponConfig,
                 {"name": "Cursed Blade", "atk_bonus": -5, "price": 0},
                 "atk_bonus=-5 (Field ge=0 missing)")
    _should_fail(WeaponConfig,
                 {"name": "Priceless Gem", "atk_bonus": 0, "price": -100},
                 "price=-100 (Field ge=0 missing)")
    _should_fail(WeaponConfig,
                 {"atk_bonus": 3, "price": 50},
                 "name missing")

    print("✅ Mission 02 complete — MonsterConfig and WeaponConfig validate all constraints.")
    update_progress("02_pydantic_monster_config")


if __name__ == "__main__":
    main()
