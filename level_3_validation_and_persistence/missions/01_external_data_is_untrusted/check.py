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


def main() -> None:
    task_path = Path(__file__).parent / "task.py"

    # Import student module
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

    # Load broken monsters
    broken_file = Path(__file__).parent / "broken_monsters.json"
    with open(broken_file) as f:
        monsters = json.load(f)["monsters"]

    # Goblin (index 0) is valid
    errors = fn(monsters[0])
    if errors:
        print(f"❌ Goblin should be valid but got errors: {errors}")
        raise SystemExit(1)

    # Ghost (index 1): hp is -50 — must catch negative hp
    errors = fn(monsters[1])
    if not any("hp" in e.lower() for e in errors):
        print("❌ Ghost has hp=-50 but validate_monster() did not report an hp error.")
        raise SystemExit(1)

    # Slime (index 2): hp is "lots" (str) — must catch wrong type
    errors = fn(monsters[2])
    if not any("hp" in e.lower() for e in errors):
        print('❌ Slime has hp="lots" (str) but validate_monster() did not report an hp error.')
        raise SystemExit(1)

    # Bandit (index 3): hp is missing — must catch missing field
    errors = fn(monsters[3])
    if not any("hp" in e.lower() for e in errors):
        print("❌ Bandit is missing 'hp' but validate_monster() did not report an hp error.")
        raise SystemExit(1)

    # Ogre (index 4): has extra field "secret_power" — should still be valid
    errors = fn(monsters[4])
    if errors:
        print(f"❌ Ogre has an unknown extra field but should still be considered valid. Got: {errors}")
        raise SystemExit(1)

    print("✅ Mission 01 complete — validate_monster() catches all four problems.")
    update_progress("01_external_data_is_untrusted")


if __name__ == "__main__":
    main()
